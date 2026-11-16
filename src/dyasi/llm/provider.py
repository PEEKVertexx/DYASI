from abc import ABC, abstractmethod
from dataclasses import dataclass
from beartype import beartype
from dyasi.exceptions import MissingPropertyError, InappropiratePropertyError, InvalidTaskError
from dyasi.http.models import Request
import dyasi.llm.router as router

TASKS = ["triage", "vulnerability_test", "detect_false_positive", "reporting"]
TASKS_LENGTH = len(TASKS)


def get_llm_providers(self):
    pass

class Provider(ABC):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # Checking if the "MODEL_RATE" property exists
        if "MODEL_RATE" in cls.__dict__:
            # Checking the value of the property
            
            ## Checking if it's an integer or a float
            if isinstance(cls.MODEL_RATE, int) or isinstance(cls.MODEL_RATE, float):
                # Checking if it's a truthy
                if not cls.MODEL_RATE:
                    raise InappropiratePropertyError("The MODEL_RATE couldn't be zero!")
                # Checking if it's negative
                if cls.MODEL_RATE < 0:
                    raise InappropiratePropertyError("The MODEL_RATE must be a positive number!")
            else:
                raise InappropiratePropertyError("The MODEL_RATE must be an integer or a float")
        else:
            raise MissingPropertyError(f"The property MODEL_RATE is not defined in {cls.__name__} class at llm/providers")


    @abstractmethod
    def generate(self):
        pass

    @abstractmethod
    def get_grade(self):
        pass

# NOTE: This Generate class is the main interface to communicate with LLMs in the DYASI, meanwhile the generate method inside the LLM provider classes is used for communicating with a particular model
@beartype
@dataclass
class Generate:
    task: str | int

    def __post_init__(self):
        # Checking the task

        ## Checking if the user wants to use number-based task seletion feature
        if isinstance(self.task, int):
            # Checking if the number being out of the range
            if self.task > TASKS_LENGTH:
                raise InvalidTaskError(f"The task that you've selected by its number is even higher than available tasks, Available tasks are {TASKS_LENGTH} and their numeric identifiers:\n\n{"\n".join([f"{index}. {task}" for index, task in enumerate(TASKS)])}")
            elif self.task < 1:
                raise InvalidTaskError(f"The task that you've selected by its number is even higher than available tasks, Available tasks are {TASKS_LENGTH} and their numeric identifiers:\n\n{"\n".join([f"{index}. {task}" for index, task in enumerate(TASKS)])}")

            self.task = TASKS[self.task]


        ## Checking if the user wants to use text-based task selection feature
        elif self.task not in TASKS:
            raise InvalidTaskError(f"Your provided task is invalid! available tasks are: {", ".join(TASKS)}")

        # Specifyinc the best LLM based on the task
        specified_model = router.Engine()

    def ask_llm(self, prompt: str | list[Request]):
        pass