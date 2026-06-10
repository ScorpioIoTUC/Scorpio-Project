#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lora_spectrogram.py
-------------------
Lee un archivo IQ grabado con rtl_sdr y grafica:
  - Panel superior: potencia integrada en banda vs tiempo (para ubicar la recepcion)
  - Panel inferior: espectrograma (frecuencia vs tiempo) de las ventanas activas,
    donde se pueden ver los chirps LoRa como rampas diagonales.

Uso:
    python lora_spectrogram.py archivo.iq
    python lora_spectrogram.py archivo.iq --fc 137.1 --fs 0.25 --lora-fc 137.055 --lora-bw 0.0417
    python lora_spectrogram.py archivo.iq --fft-size 1024 --sigma 2 --save

Parametros:
    --fc        Frecuencia central de grabacion (MHz)        [default: 137.1]
    --fs        Sampling rate del archivo (MS/s)             [default: 0.25]
    --lora-fc   Frecuencia central de la senal (MHz)         [default: 137.055]
    --lora-bw   Ancho de banda de la senal (MHz)             [default: 0.0417]
    --window    Duracion de cada ventana de deteccion (s)    [default: 0.5]
    --fft-size  Tamano FFT del espectrograma (muestras)      [default: 512]
    --overlap   Solapamiento entre FFTs del espectrograma    [default: 0.75]
    --sigma     Multiplicador sigma para el umbral           [default: 2.0]
    --margin    Margen extra fuera de la banda LoRa (kHz)    [default: 20]
    --save      Guardar figura como PNG junto al archivo IQ
"""

import sys
import argparse
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker


# ============================================================
# CONFIGURACION POR DEFECTO
# ============================================================

DEFAULT_FC_MHZ   = 137.1
DEFAULT_FS_MSPS  = 0.25
DEFAULT_LORA_FC  = 137.055
DEFAULT_LORA_BW  = 0.0417
DEFAULT_WINDOW_S = 0.5
DEFAULT_FFT_SIZE = 512
DEFAULT_OVERLAP  = 0.75
DEFAULT_SIGMA    = 2.0
DEFAULT_MARGIN   = 20.0   # kHz extra a cada lado de la banda LoRa en el espectrograma
DEFAULT_CONTEXT  = 1      # ventanas de contexto antes y despues de las activas


# ============================================================
# LECTURA IQ
# ============================================================

def load_iq(filepath: Path, fs: float):
    if filepath.suffix.lower() in (".cf32", ".cfile"):
        # float32 intercalado: I0 Q0 I1 Q1 ...
        raw     = np.fromfile(filepath, dtype=np.float32)
        if len(raw) % 2 != 0:
            raw = raw[:-1]
        samples = raw[0::2] + 1j * raw[1::2]
    else:
        # uint8 intercalado (rtl_sdr): centrado en 127.5
        raw = np.fromfile(filepath, dtype=np.uint8)
        if len(raw) % 2 != 0:
            raw = raw[:-1]
        iq      = raw.astype(np.float32) - 127.5
        iq     /= 127.5
        samples = iq[0::2] + 1j * iq[1::2]

    duration = len(samples) / fs
    return samples, duration


# ============================================================
# DETECCION DE VENTANAS ACTIVAS (misma logica que los otros scripts)
# ============================================================

def detect_active_windows(samples, fs, center_offset, bandwidth, window_samples, sigma):
    n_windows = len(samples) // window_samples
    freqs     = np.fft.fftfreq(window_samples, d=1.0 / fs)
    f_low     = center_offset - bandwidth / 2
    f_high    = center_offset + bandwidth / 2
    band_mask = (freqs >= f_low) & (freqs <= f_high)
    hann      = np.hanning(window_samples)
    power_db  = np.zeros(n_windows)
    t_axis    = np.zeros(n_windows)

    for i in range(n_windows):
        seg          = samples[i * window_samples:(i + 1) * window_samples]
        spectrum     = np.fft.fft(seg * hann)
        power_db[i]  = 10 * np.log10(np.mean(np.abs(spectrum[band_mask]) ** 2) + 1e-30)
        t_axis[i]    = (i + 0.5) * window_samples / fs

    p_mean    = np.mean(power_db)
    p_std     = np.std(power_db)
    threshold = p_mean + sigma * p_std
    above_idx = np.where(power_db >= threshold)[0]

    return t_axis, power_db, threshold, above_idx


# ============================================================
# ESPECTROGRAMA
# ============================================================

def compute_spectrogram(samples, fs, center_offset, bandwidth,
                        window_samples, above_idx,
                        fft_size, overlap, margin_hz, context):
    """
    Calcula el espectrograma STFT de las muestras activas mas 'context'
    ventanas de contexto antes y despues de cada grupo de ventanas activas.

    Retorna:
        t_spec      : eje de tiempo (s, relativo al inicio del primer segmento)
        f_rel       : frecuencias relativas al centro de grabacion (Hz)
        Sxx_db      : matriz espectrograma en dB, shape (n_freqs, n_times)
        t_offset    : tiempo absoluto del inicio del primer segmento (s)
        context_idx : indices de above_idx expandidos que son solo contexto
                      (para marcarlos distinto en el plot)
    """
    if len(above_idx) == 0:
        return None, None, None, None, None

    n_windows = len(samples) // window_samples

    # Expandir above_idx con 'context' ventanas antes y despues de cada grupo,
    # respetando los limites del archivo. Usar un set para evitar duplicados.
    expanded = set(above_idx.tolist())
    for idx in above_idx:
        for delta in range(1, context + 1):
            if idx - delta >= 0:
                expanded.add(idx - delta)
            if idx + delta < n_windows:
                expanded.add(idx + delta)

    above_set   = set(above_idx.tolist())
    context_set = expanded - above_set          # solo las ventanas de contexto
    all_idx     = np.array(sorted(expanded))    # indices ordenados para concatenar

    hop  = int(fft_size * (1 - overlap))
    hann = np.hanning(fft_size)

    t_offset = all_idx[0] * window_samples / fs
    active   = np.concatenate([
        samples[i * window_samples:(i + 1) * window_samples]
        for i in all_idx
    ])

    # STFT
    n_frames = (len(active) - fft_size) // hop + 1
    Sxx      = np.zeros((fft_size, n_frames), dtype=np.float32)

    for k in range(n_frames):
        seg       = active[k * hop: k * hop + fft_size]
        spectrum  = np.fft.fft(seg * hann)
        Sxx[:, k] = np.abs(np.fft.fftshift(spectrum)) ** 2

    Sxx_db = 10 * np.log10(Sxx + 1e-30)
    t_spec = np.arange(n_frames) * hop / fs

    f_rel = np.fft.fftshift(np.fft.fftfreq(fft_size, d=1.0 / fs))

    # Calcular los tiempos absolutos de inicio/fin de las ventanas de contexto
    # para poder marcarlos en el plot
    context_times = sorted([i * window_samples / fs for i in context_set])

    return t_spec, f_rel, Sxx_db, t_offset, context_times


# ============================================================
# GRAFICACION
# ============================================================

def plot_results(t_axis, power_db, threshold, above_idx,
                 t_spec, f_rel, Sxx_db, t_offset, context_times,
                 filepath, args):

    fc_mhz      = args.fc
    lora_fc_mhz = args.lora_fc
    lora_bw_khz = args.lora_bw * 1e3

    fig = plt.figure(figsize=(14, 9))
    fig.patch.set_facecolor("#0d1117")
    gs  = gridspec.GridSpec(2, 1, figure=fig, hspace=0.4, height_ratios=[1, 2])

    ax_pow = fig.add_subplot(gs[0])
    ax_spc = fig.add_subplot(gs[1])

    for ax in [ax_pow, ax_spc]:
        ax.set_facecolor("#161b22")
        ax.tick_params(colors="#8b949e", labelsize=9)
        for spine in ax.spines.values():
            spine.set_color("#30363d")
        ax.yaxis.label.set_color("#8b949e")
        ax.xaxis.label.set_color("#8b949e")
        ax.title.set_color("#e6edf3")

    # ----------------------------------------------------------
    # Panel superior: potencia en banda vs tiempo
    # ----------------------------------------------------------
    p_min = np.min(power_db)
    p_max = np.max(power_db)

    ax_pow.plot(t_axis, power_db, color="#58a6ff", lw=0.8, alpha=0.85)
    ax_pow.fill_between(t_axis, p_min - 5, power_db, color="#1f6feb", alpha=0.15)
    ax_pow.axhline(threshold, color="#f0883e", lw=1.2, ls="--", alpha=0.8,
                   label=f"Umbral ({args.sigma:.1f}sigma) = {threshold:.1f} dB")
    ax_pow.axhline(np.mean(power_db), color="#8b949e", lw=0.8, ls=":",
                   alpha=0.7, label=f"Media = {np.mean(power_db):.1f} dB")

    if len(above_idx) > 0:
        above_mask = np.zeros(len(t_axis), dtype=bool)
        above_mask[above_idx] = True
        ax_pow.fill_between(t_axis, p_min - 5, power_db,
                            where=above_mask, color="#3fb950", alpha=0.35,
                            label=f"Ventanas activas ({len(above_idx)})")

    ax_pow.set_xlim(t_axis[0], t_axis[-1])
    ax_pow.set_ylim(p_min - 8, p_max + 8)
    ax_pow.set_xlabel("Tiempo (s)", fontsize=9)
    ax_pow.set_ylabel("Potencia banda (dB)", fontsize=9)
    ax_pow.set_title(
        f"Potencia en banda  —  {lora_fc_mhz:.3f} MHz +/- {lora_bw_khz/2:.1f} kHz  "
        f"({filepath.name})",
        fontsize=10, fontweight="bold"
    )
    ax_pow.legend(loc="upper right", fontsize=8,
                  facecolor="#161b22", edgecolor="#30363d", labelcolor="#e6edf3")
    ax_pow.grid(True, color="#30363d", alpha=0.5, lw=0.6)

    # ----------------------------------------------------------
    # Panel inferior: espectrograma de ventanas activas
    # ----------------------------------------------------------
    if t_spec is None:
        ax_spc.text(0.5, 0.5, "Sin ventanas sobre el umbral\n— no hay espectrograma",
                    ha="center", va="center", color="#8b949e", fontsize=11,
                    transform=ax_spc.transAxes)
    else:
        # Frecuencia absoluta: fc_mhz + f_rel / 1e6
        # Ejemplo: fc=137.1, f_rel=-45000 Hz -> 137.1 + (-0.045) = 137.055 MHz
        f_abs_mhz = fc_mhz + f_rel / 1e6
        f_lo_mhz  = lora_fc_mhz - (args.lora_bw / 2) - (args.margin / 1e3)
        f_hi_mhz  = lora_fc_mhz + (args.lora_bw / 2) + (args.margin / 1e3)
        band_mask = (f_abs_mhz >= f_lo_mhz) & (f_abs_mhz <= f_hi_mhz)

        f_plot   = f_abs_mhz[band_mask]
        Sxx_plot = Sxx_db[band_mask, :]

        # Tiempo absoluto en el eje X
        t_plot = t_spec + t_offset

        # Rango de color: percentil 5-99 para no saturar con ruido
        vmin = np.percentile(Sxx_plot, 5)
        vmax = np.percentile(Sxx_plot, 99)

        im = ax_spc.pcolormesh(
            t_plot, f_plot, Sxx_plot,
            cmap="inferno", shading="auto",
            vmin=vmin, vmax=vmax,
            rasterized=True,
        )

        # Colorbar
        cbar = fig.colorbar(im, ax=ax_spc, pad=0.01, fraction=0.025)
        cbar.set_label("PSD (dB)", color="#8b949e", fontsize=8)
        cbar.ax.tick_params(colors="#8b949e", labelsize=7)

        # Marcar bordes de banda LoRa
        ax_spc.axhline(lora_fc_mhz - args.lora_bw / 2, color="#3fb950",
                       lw=1.0, ls="--", alpha=0.7, label=f"Banda LoRa ({lora_bw_khz:.1f} kHz)")
        ax_spc.axhline(lora_fc_mhz + args.lora_bw / 2, color="#3fb950",
                       lw=1.0, ls="--", alpha=0.7)
        ax_spc.axhline(lora_fc_mhz, color="#3fb950",
                       lw=0.6, ls=":", alpha=0.5)

        ax_spc.set_xlim(t_plot[0], t_plot[-1])
        ax_spc.set_ylim(f_lo_mhz, f_hi_mhz)

        # Marcar ventanas de contexto con banda vertical semitransparente
        win_s = args.window   # duracion de una ventana de deteccion en segundos
        for t_ctx in context_times:
            ax_spc.axvspan(t_ctx + t_offset, t_ctx + t_offset + win_s,
                           color="#8b949e", alpha=0.12, zorder=0)

        # Eje Y en kHz relativo al centro LoRa para facil lectura
        def mhz_to_rel_khz(x, _):
            return f"{(x - lora_fc_mhz) * 1e3:+.0f}"
        ax_spc.yaxis.set_major_formatter(ticker.FuncFormatter(mhz_to_rel_khz))

        ax_spc.set_xlabel("Tiempo (s)", fontsize=9)
        ax_spc.set_ylabel(f"Frecuencia rel. a {lora_fc_mhz:.3f} MHz (kHz)", fontsize=9)
        ax_spc.set_title(
            f"Espectrograma — FFT {args.fft_size} pts  |  "
            f"overlap {args.overlap*100:.0f}%  |  "
            f"resolucion {args.fs*1e6/args.fft_size:.1f} Hz/bin",
            fontsize=10, fontweight="bold"
        )
        ax_spc.legend(loc="upper right", fontsize=8,
                      facecolor="#0d1117", edgecolor="#30363d", labelcolor="#e6edf3")
        ax_spc.grid(True, color="#ffffff", alpha=0.05, lw=0.4)

        # Info box
        res_hz   = args.fs * 1e6 / args.fft_size
        hop_s    = args.fft_size * (1 - args.overlap) / (args.fs * 1e6)
        ax_spc.text(0.01, 0.97,
                    f"Res. freq : {res_hz:.1f} Hz/bin\n"
                    f"Res. tiempo: {hop_s*1e3:.2f} ms/frame\n"
                    f"Ventanas activas: {len(above_idx)}\n"
                    f"Contexto (+/-{args.context}): {len(context_times)} ventanas",
                    transform=ax_spc.transAxes, fontsize=7.5,
                    verticalalignment="top", color="#8b949e",
                    fontfamily="monospace",
                    bbox=dict(boxstyle="round,pad=0.4", facecolor="#0d1117",
                              edgecolor="#30363d", alpha=0.85))

    return fig


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Espectrograma de ventanas activas en banda LoRa de un archivo IQ"
    )
    parser.add_argument("filepath",   type=Path)
    parser.add_argument("--fc",       type=float, default=DEFAULT_FC_MHZ,
                        help=f"Frecuencia central de grabacion (MHz) [default: {DEFAULT_FC_MHZ}]")
    parser.add_argument("--fs",       type=float, default=DEFAULT_FS_MSPS,
                        help=f"Sampling rate (MS/s) [default: {DEFAULT_FS_MSPS}]")
    parser.add_argument("--lora-fc",  type=float, default=DEFAULT_LORA_FC, dest="lora_fc",
                        help=f"Frecuencia central de la senal (MHz) [default: {DEFAULT_LORA_FC}]")
    parser.add_argument("--lora-bw",  type=float, default=DEFAULT_LORA_BW, dest="lora_bw",
                        help=f"Ancho de banda (MHz) [default: {DEFAULT_LORA_BW}]")
    parser.add_argument("--window",   type=float, default=DEFAULT_WINDOW_S,
                        help=f"Duracion de ventana de deteccion (s) [default: {DEFAULT_WINDOW_S}]")
    parser.add_argument("--fft-size", type=int,   default=DEFAULT_FFT_SIZE, dest="fft_size",
                        help=f"Tamano FFT del espectrograma [default: {DEFAULT_FFT_SIZE}]")
    parser.add_argument("--overlap",  type=float, default=DEFAULT_OVERLAP,
                        help=f"Solapamiento entre FFTs (0-1) [default: {DEFAULT_OVERLAP}]")
    parser.add_argument("--sigma",    type=float, default=DEFAULT_SIGMA,
                        help=f"Multiplicador sigma para umbral [default: {DEFAULT_SIGMA}]")
    parser.add_argument("--margin",   type=float, default=DEFAULT_MARGIN,
                        help=f"Margen extra fuera de banda LoRa (kHz) [default: {DEFAULT_MARGIN}]")
    parser.add_argument("--context",  type=int,   default=DEFAULT_CONTEXT,
                        help=f"Ventanas de contexto antes y despues de las activas "
                             f"[default: {DEFAULT_CONTEXT}]")
    parser.add_argument("--save",     action="store_true",
                        help="Guardar figura como PNG junto al archivo IQ")
    args = parser.parse_args()

    if not args.filepath.exists():
        print(f"ERROR: No se encontro el archivo '{args.filepath}'")
        sys.exit(1)

    fs             = args.fs * 1e6
    lora_bw_hz     = args.lora_bw * 1e6
    center_offset  = (args.lora_fc - args.fc) * 1e6
    window_samples = int(args.window * fs)
    margin_hz      = args.margin * 1e3

    nyquist = fs / 2
    if abs(center_offset) + lora_bw_hz / 2 > nyquist:
        print("ERROR: La banda de interes esta fuera del ancho de banda capturado.")
        sys.exit(1)

    print(f"Archivo  : {args.filepath}  ({args.filepath.stat().st_size/1e6:.1f} MB)")
    print(f"SR       : {args.fs*1e3:.0f} kSps   |   BW capturado: +/-{nyquist/1e3:.1f} kHz")
    print(f"Banda    : {args.lora_fc:.3f} MHz +/- {lora_bw_hz/2e3:.2f} kHz  "
          f"(offset {center_offset/1e3:+.2f} kHz)")
    print(f"FFT      : {args.fft_size} pts  ->  {fs/args.fft_size:.1f} Hz/bin  |  "
          f"overlap {args.overlap*100:.0f}%")

    print("Cargando muestras...")
    samples, duration = load_iq(args.filepath, fs)
    print(f"  {len(samples):,} muestras — {duration:.1f} s")

    print("Detectando ventanas activas...")
    t_axis, power_db, threshold, above_idx = detect_active_windows(
        samples, fs, center_offset, lora_bw_hz, window_samples, args.sigma
    )
    print(f"  Umbral ({args.sigma:.1f}sigma): {threshold:.1f} dB")
    print(f"  Ventanas activas: {len(above_idx)} / {len(t_axis)}")
    if len(above_idx) > 0:
        print(f"  Rango temporal : {t_axis[above_idx[0]]:.1f} s — "
              f"{t_axis[above_idx[-1]]:.1f} s")

    print("Calculando espectrograma...")
    t_spec, f_rel, Sxx_db, t_offset, context_times = compute_spectrogram(
        samples, fs, center_offset, lora_bw_hz,
        window_samples, above_idx,
        args.fft_size, args.overlap, margin_hz, args.context
    )
    if context_times is not None:
        print(f"  Contexto (+/-{args.context} ventanas): {len(context_times)} adicionales")

    fig = plot_results(
        t_axis, power_db, threshold, above_idx,
        t_spec, f_rel, Sxx_db, t_offset, context_times,
        args.filepath, args
    )

    if args.save:
        out_path = args.filepath.with_suffix(".spectrogram.png")
        fig.savefig(out_path, dpi=150, bbox_inches="tight",
                    facecolor=fig.get_facecolor())
        print(f"Figura guardada: {out_path}")

    plt.show()


if __name__ == "__main__":
    main()