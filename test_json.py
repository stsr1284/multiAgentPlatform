json_data = """
{
  "agent_list": [
    {
      "orchestration": {
        "type": "supervisoragentbuilder",
        "llm": "gpt-4o-mini",
        "prompt": "str",
        "name": "testsupervisor1",
        "agent_list": [
          {
            "agent": {
              "type": "reactagentbuilder",
              "llm": "gpt-4o-mini",
              "tool": "research_tool",
              "name": "test1",
              "description": null,
              "prompt": null,
              "config": null
            }
          },
          {
            "agent": {
              "type": "reactagentbuilder",
              "llm": "gpt-4o-mini",
              "tool": "research_tool",
              "name": "test2",
              "description": null,
              "prompt": null,
              "config": null
            }
          },
          {
            "orchestration": {
              "type": "supervisoragentbuilder",
              "llm": "gpt-4o-mini",
              "prompt": "str",
              "name": "testsupervisor2",
              "agent_list": [
                {
                  "agent": {
                    "type": "reactagentbuilder",
                    "llm": "gpt-4o-mini",
                    "tool": "research_tool",
                    "name": "test3",
                    "description": null,
                    "prompt": null,
                    "config": null
                  }
                },
                {
                  "agent": {
                    "type": "reactagentbuilder",
                    "llm": "gpt-4o-mini",
                    "tool": "research_tool",
                    "name": "test4",
                    "description": null,
                    "prompt": null,
                    "config": null
                  }
                }
              ]
            }
          }
        ]
      }
    },
    {
      "agent": {
        "type": "reactagentbuilder",
        "llm": "gpt-4o-mini",
        "tool": "research_tool",
        "name": "agenttest1"
      }
    },
    {
      "agent": {
        "type": "reactagentbuilder",
        "llm": "gpt-4o-mini",
        "tool": "research_tool",
        "name": "agenttest2",
        "description": null,
        "prompt": null,
        "config": null
      }
    },
    {
      "agent": {
        "type": "reactagentbuilder",
        "llm": "gpt-4o-mini",
        "tool": "research_tool",
        "name": "testtest",
        "description": null,
        "prompt": null,
        "config": null
      }
    },
    {
      "agent": {
        "type": "reactagentbuilder",
        "llm": "gpt-4o-mini",
        "tool": "research_tool",
        "name": "testtes234234t",
        "description": null,
        "prompt": null,
        "config": null
      }
    },
    {
      "agent": {
        "type": "reactagentbuilder",
        "llm": "gpt-4o-mini",
        "tool": "research_tool",
        "name": "te234234234234sttest",
        "description": null,
        "prompt": null,
        "config": null
      }
    },
    {
      "agent": {
        "type": "reactagentbuilder",
        "llm": "gpt-4o-mini",
        "tool": "research_tool",
        "name": "agenttest3",
        "description": null,
        "prompt": null,
        "config": null
      }
    }
  ]
}

"""

카테고리, 함수 명(체크), 