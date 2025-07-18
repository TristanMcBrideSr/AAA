
import json
import re
import inspect
import os
import threading
import logging
from dotenv import load_dotenv
from pathlib import Path

from SkillsManager import SkillsManager # Dont for get to pip install SkillsManager

load_dotenv()

logger = logging.getLogger(__name__)


class SkillGraph:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(SkillGraph, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, 'initialized', False):
            return
        self._initComponents()
        self.initialized = True

    def _initComponents(self):
        self.skillsManager    = SkillsManager()
        self.showCapabilities = os.getenv('SHOW_CAPABILITIES', 'False') == 'True'
        self.showMetaData     = os.getenv('SHOW_METADATA', 'False') == 'True'
        self.loadAllComponents()
        if self.showCapabilities:
            self.getAgentCapabilities()
        if self.showMetaData:
            self.getMetaData()

    def getDir(self, *paths):
        return self.skillsManager.getDir(*paths)

    def loadAllComponents(self):
        """
        Load all components from the specified directories.
        This method loads skills and tools from the 'Skills' directory.
        """
        self.agentSkills = []
        self.agentTools = []

        self.skillsManager.loadComponents(
            paths=[
                ['Skills'],
            ],
            components=[
                self.agentSkills,
            ],
            reloadable=[
                False,
            ]
        )

    def getAgentActions(self):
        """
        Get self actions based on the skills available.
        This method combines dynamic, static, and restricted self skills.
        """
        skills = (
            self.agentSkills
        )
        return self.skillsManager.getComponents(skills)

    def reloadSkills(self):
        """
        Reload all skills and print any new skills added.
        """
        original = self.getMetaData()
        self.skillsManager.reloadSkills()
        new = self.getMetaData()
        for skill in new:
            if skill not in original:
                print(f"I've added the new skill {skill['className']} That {skill['description']}.\n")

    def getMetaData(self):
        """Get metadata for all skills."""
        metaData = (
                self.agentSkills
        )
        return self.skillsManager.getMetaData(metaData, self.showMetaData)

    # ----- Skills -----
    def getAgentCapabilities(self):
        """
        Get the capabilities of the agent based on its skills.
        This method retrieves the capabilities of the agent's skills and returns them in a structured format.
        """
        description = False
        capabitites = (
            self.agentSkills
        )
        return self.skillsManager.getCapabilities(capabitites, self.showCapabilities, description)

    def checkActions(self, action: str) -> str:
        """
        Check if the given action is valid based on the agent's skills.
        Returns a string indicating whether the action is valid or not.
        """
        return self.skillsManager.actionParser.checkActions(action)

    def getActions(self, action: str) -> list:
        """
        Get a list of actions based on the given action string.
        This method uses the skills manager's action parser to retrieve actions that match the given string.
        If the action is not found, it returns an empty list.
        """
        return self.skillsManager.actionParser.getActions(action)

    def executeAction(self, actions, action):
        """
        Execute a single action based on the provided actions and action string.
        You must create your own for loop if you want to execute multiple actions.
        """
        return self.skillsManager.actionParser.executeAction(actions, action)

    def executeActions(self, actions, action):
        """
        Execute both single and multiple actions based on the provided actions and action string.
        The for loop is handled internally, so you can pass a single action or a list of actions.
        """
        return self.skillsManager.actionParser.executeActions(actions, action)

    def skillInstructions(self):
        """
        Get skill instructions for the agent based on its capabilities.
        """
        skillExamples = self.skillExamples()
        return self.skillsManager.skillInstructions(self.getAgentCapabilities(), skillExamples)

    def skillExamples(self):
        """
        Get examples of how to use skills from your naming conventions.
        This should be customized to match your skill naming conventions.
        """
        return (
            "Single Action Examples:\n" # Don't change this line
            "- ['getDate()']\n" # Change to match your skill naming conventions
            "- ['getTime()']\n" # Change to match your skill naming conventions
            "- ['getDate()', 'getTime()']\n" # Change to match your skill naming conventions

            "Skill With Sub-Action Examples:\n" # Don't change this line
            "- ['appSkill(\"open\", \"Notepad\")']\n" # Change to match your skill naming conventions
            "- ['appSkill(\"open\", \"Notepad\")', 'appSkill(\"open\", \"Word\")']\n"
            "- ['weatherSkill(\"get-weather\", \"47.6588\", \"-117.4260\")']\n" # Change to match your skill naming conventions
        )


    # ----- Tools -----
    def executeTool(self, name, tools, args, threshold=80, retry=True):
        """
        Execute a tool with the given name, tools, and arguments.
        If the tool is not found, it will return an error message.
        If the tool execution fails, it will retry based on the retry parameter.
        """
        return self.skillsManager.actionParser.executeTool(name, tools, args, threshold, retry)

    def getTools(self):
        """
        Get all tools available for the agent.
        """
        tools = (
            self.agentTools
        )
        return self.skillsManager.getTools(tools)

    def extractJson(self, text):
        """
        Extract the first JSON array or object from a string, even if wrapped in markdown or extra commentary.
        """
        return self.skillsManager.extractJson(text)

    def getJsonSchema(self, func, schemaType):
        """
        Build a json schema for a function based on its signature and docstring metadata.
        The schemaType can be either 'completions' or 'responses'.
        Compatible with the OpenAI API and similar services that use JSON schemas.
        Returns a dictionary representing the schema.
        """
        return self.skillsManager.getJsonSchema(func, schemaType)

    def getTypedSchema(self, func):
        """
        Build a typed schema for a function based on its signature and docstring metadata.
        Compatible with the Google API.
        Returns a dictionary representing the schema.
        """
        return self.skillsManager.getTypedSchema(func)

    # ----- Can be used with both skills and tools -----
    def isStructured(self, *args):
        """
        Check if any of the arguments is a list of dictionaries.
        This indicates structured input (multi-message format).
        """
        return self.skillsManager.isStructured(*args)

    def handleTypedFormat(self, role: str = "user", content: str = ""):
        """
        Format content for Google GenAI APIs.
        """
        return self.skillsManager.handleTypedFormat(role, content)

    def handleJsonFormat(self, role: str = "user", content: str = ""):
        """
        Format content for OpenAI APIs and similar JSON-based APIs.
        """
        return self.skillsManager.handleJsonFormat(role, content)

    def buildGoogleSafetySettings(self, harassment="BLOCK_NONE", hateSpeech="BLOCK_NONE", sexuallyExplicit="BLOCK_NONE", dangerousContent="BLOCK_NONE"):
        """
        Construct a list of Google GenAI SafetySetting objects.
        """
        return self.skillsManager.buildGoogleSafetySettings(harassment, hateSpeech, sexuallyExplicit, dangerousContent)

