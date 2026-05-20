from pathlib import Path


class TopicValidator:
    """Loads and validates MQTT topics defined in configs/mqtt/topics.yaml."""

    def __init__(self, topics_file: Path | None = None) -> None:
        self._topics_file = topics_file or self._default_topics_file()
        self._allowed_topics = self._load_allowed_topics()

    @staticmethod
    def _default_topics_file() -> Path:
        return Path(__file__).resolve().parents[4] / "configs" / "mqtt" / "topics.yaml"

    @staticmethod
    def _clean_yaml_value(value: str) -> str:
        return value.strip().strip('"').strip("'")

    def _load_allowed_topics(self) -> set[str]:
        """Load topic values from topics.yaml and resolve namespace placeholders."""

        if not self._topics_file.exists():
            msg = f"Topics file not found: {self._topics_file}"
            raise FileNotFoundError(msg)

        namespace = ""
        topic_values: list[str] = []

        for raw_line in self._topics_file.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or ":" not in line:
                continue

            key, raw_value = line.split(":", maxsplit=1)
            value = self._clean_yaml_value(raw_value)

            if key.strip() == "namespace":
                namespace = value
                continue

            if value and ("/" in value or "{namespace}" in value):
                topic_values.append(value)

        return {topic.replace("{namespace}", namespace) for topic in topic_values}

    @property
    def allowed_topics(self) -> set[str]:
        return set(self._allowed_topics)

    def validate(self, topic: str, action: str) -> None:
        if topic not in self._allowed_topics:
            allowed = ", ".join(sorted(self._allowed_topics))
            msg = (
                f"Invalid topic for {action}: '{topic}'. "
                f"Allowed topics from configs/mqtt/topics.yaml: {allowed}"
            )
            raise ValueError(msg)
