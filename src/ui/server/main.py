import json, os, subprocess
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from http import HTTPStatus
from pathlib import Path
import logging

# Logger configs
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Server configs
PORT = 8000
SERVER_URL = f"http://localhost:{PORT}"
UI_URL = "http://127.0.0.1:3000"
UI_DIR = Path(__file__).parent.parent
SYSTEM_JSON_PATH = UI_DIR / "server/system.json"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.system_json = self._load_system_json()
        super().__init__(*args, directory=str(UI_DIR), **kwargs)

    def _load_system_json(self) -> dict:
        # Loading system json from its path
        with open(SYSTEM_JSON_PATH, "r") as f:
            return json.load(f)

    def _update_system_json(self):
        # Update the system json with new data
        current_data = self.system_json
        with open(SYSTEM_JSON_PATH, "w") as f:
            json.dump(current_data, f, indent=4)

    def _get_steps_index(self) -> dict:
        # Create a dictionary with the index of each step in the steps array
        return {
            item["name"]: index for index, item in enumerate(self.system_json["steps"])
        }

    def _check_previous_steps(self, step_name: str) -> bool:
        # first we get the index of the step in the steps array
        steps_index = self._get_steps_index()
        step_index = steps_index[step_name]
        # then we get the steps array
        steps = self.system_json["steps"]
        # then we check if all the previous steps are completed
        previous_steps = [
            step for step in steps[:step_index] if step["status"] == False
        ]
        if previous_steps:
            logging.warning("Previous steps not completed: %s", previous_steps)
            return False
        return True

    def _body(self) -> dict:
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        return json.loads(body) if body else {}

    def _get_default(self) -> dict:
        return {"message": "Welcome to the Scorpio setup server."}

    def _get_system_state(self) -> dict:
        logging.info("Getting system state")

        steps = [item["status"] for item in self.system_json["steps"]]
        if all(step == True for step in steps):
            # The system is fully set up, return completed state
            return {"completed": True, "current_step": None}
        # The system is not fully set up, return the current step
        current_step = self._get_current_step()
        return {"completed": False, **current_step}

    def _get_current_step(self) -> dict:
        logging.info("Getting current step")
        steps = [(item["name"], item["status"]) for item in self.system_json["steps"]]
        # find the first step that is not completed
        for step in steps:
            if not step[1]:
                return {"current_step": step[0]}
        return {"current_step": "All steps completed"}

    def do_GET(self):
        if self.path == "/api/status":
            return self.send_json(self._get_system_state(), HTTPStatus.OK)
        elif self.path == "/api/current_step":
            return self.send_json(self._get_current_step(), HTTPStatus.OK)
        else:
            return self.send_json(self._get_default(), HTTPStatus.OK)

    def do_POST(self):
        if self.path != "/api/confirm_step":
            self.send_json({"error": "Invalid route."}, HTTPStatus.NOT_FOUND)
            return

        body = self._body()
        step = body.get("step", "")
        steps_names = [step["name"] for step in self.system_json["steps"]]

        # Review if the step exist
        if step not in steps_names:
            self.send_json(
                {"error": "Invalid step.", "steps": steps_names}, HTTPStatus.NOT_FOUND
            )
            return
        # Review if the step is already completed
        step_data = next(
            item for item in self.system_json["steps"] if item["name"] == step
        )
        if step_data["status"]:
            next_step = self._get_current_step().get("current_step")
            self.send_json(
                {"error": "Step is already completed.", "next_step": next_step},
                HTTPStatus.BAD_REQUEST,
            )
            return

        # Review if previous steps are completed
        if not self._check_previous_steps(step):
            self.send_json(
                {"error": "Previous steps are not completed."},
                HTTPStatus.BAD_REQUEST,
            )
            return

        # Execute the command associated with the step
        command = step_data["command"]
        try:
            logging.info("Executing command for step '%s': %s", step, command)
            logging.info("Mocking command ...")
            # subprocess.run(command, shell=True, check=True)

            # Extract the step index and update the system json with the new status
            step_index = self._get_steps_index()[step]
            step_data["status"] = True
            self.system_json["steps"][step_index] = step_data
            self._update_system_json()
            self.send_json(
                {"message": f"Step '{step}' executed successfully."}, HTTPStatus.OK
            )
        except subprocess.CalledProcessError as e:
            logging.error("Error executing command for step '%s': %s", step, e)
            self.send_json(
                {"error": f"Error executing step '{step}': {e}"},
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )
            return

    def send_json(self, payload, status=200):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", UI_URL)
        super().end_headers()


def run_server():

    logging.info("Server started at %s", SERVER_URL)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()


if __name__ == "__main__":
    run_server()
