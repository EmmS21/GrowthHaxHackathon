from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
from dotenv import load_dotenv
import tweepy

load_dotenv()

class AIMarketing:
    def getText(self, scrappedOutput):
        openai_api_key = os.getenv("OPENAI_API_KEY")
        twitter_api_key = os.getenv("X_API_KEY")
        twitter_secret = os.getenv("X_SECRET")
        auth = tweepy.OAuth1UserHandler(twitter_api_key, twitter_secret)
        api = tweepy.API(auth)
        llm = ChatOpenAI(model="gpt-4o", openai_api_key=openai_api_key, temperature=0)
        input_data = {
            "input": scrappedOutput,
            "agent_scratchpad": ""
        }
        @tool
        def search_tweets(keywords, count=10):
            """
            Search for tweets containing specific keywords and return their text content.

            Args:
                keywords (str): Keywords to search for in tweets.
                count (int, optional): Number of tweets to retrieve (default is 10).

            Returns:
                list: List of tweet texts.
            """
            try:
                tweets = tweepy.Cursor(api.search_tweets, q=keywords, lang="en").items(count)
                return [tweet.text for tweet in tweets]
            except Exception as e:
                print("Error fetching tweets", e)
                return []
        @tool
        def testing(output):
            "You don't need to use this tool as it's just a test"
            return output
        try:
            test_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", """You are an expert at marketing and listening to conversations people are having about a product. Your goal is to use tools available to understand what people are saying about problems related to our product to better align our marketing messages to different user personas
                     Instructions:
                     1. **From the text given to you, break down the problems this company solves into a concise list of problems in bullet points**
                     - structure the output as a list

                     2. **Define the target audience and their user personas**
                     - structure the output of this response as a JSON for each user persona

                     3. **Listen to conversations people are having about the problems and group these into concise themes**
                     - extract 3 appropriate keywords at most for each problem, pass the most appropriate of these into the search_tweets tool
                     - for each run, use the output from the search_tweets to create themes of conversations people are having. Group these according to the problem they fall under
                     - return a JSON with each problem and the themes under each problem based on user conversation
                     """),
                     MessagesPlaceholder("chat_history", optional=True),
                     ("human", "{input}"),
                     MessagesPlaceholder("agent_scratchpad")
                ]
            )
            toolkit = [search_tweets]
            agent = create_openai_tools_agent(llm, toolkit, test_prompt)
            agent_executor = AgentExecutor(
                agent=agent,
                tools=toolkit,
                verbose=True,
                handle_parsing_errors=True,
                max_terations=100,
                max_execution_time=189,
                return_intermediate_steps=True
            )
        except Exception as e:
            raise e
        try:
            result = agent_executor.invoke(input_data)
        except Exception as e:
            raise e
        
if __name__ == "__main__":
    scrappedOutput = """
Dagger Documentation
Welcome to Dagger, a programmable tool that lets you replace your software project's artisanal scripts with a modern API and cross-language scripting engine.

Encapsulate all your project's tasks and workflows into simple Dagger Functions, written in your programming language of choice.
Run your Dagger Functions from the command line, your language interpreter, or a custom HTTP client.
Package your Dagger Functions into a module, to reuse in your next project or share with the community.
Search for existing modules, and import them into yours. All Dagger modules can reuse each other's Dagger Functions - regardless of which language they are written in.
The Daggerverse is a free service run by Dagger, which indexes all publicly available Dagger modules, and lets you easily search and consume them.

Dagger Cloud complements Dagger Functions with a production-grade control plane. Features of Dagger Cloud include pipeline visualization, operational insights, and distributed caching.

What problem does Dagger solve?
Application delivery pipelines are a source of pain. The majority of pipelines use messy, hard-to-debug YAML, which is not portable across CI providers, and inconsistent shell scripts, which may not work consistently across environments and platforms. Developers have to "push and pray" - instead of being able to test and build code locally and seeing near-instant feedback from their delivery pipelines, they have to wait (and hope) for a green signal from pipelines running on remote servers.

How does Dagger solve this problem?
Dagger solves this by running your application delivery pipelines in containers. A "Daggerized" pipeline runs the same way locally or on your CI provider, resulting in faster feedback to the developer and the elimination of last-minute surprises. Dagger also caches everything, which accelerates each pipeline run significantly and often cuts run times by over 50%. And finally, Dagger supports multiple programming languages via native-language SDKs, enabling developers to build their delivery pipelines in the same language as their application and benefit from the ecosystem's existing tooling and best practices.

Who is Dagger for?
Dagger may be a good fit if you are...

Your team's "designated devops person", hoping to replace a pile of artisanal scripts with something more powerful.
A platform engineer writing custom tooling, with the goal of unifying application delivery across organizational silos.
A cloud-native developer advocate or solutions engineer, looking to demonstrate a complex integration on short notice.
How does Dagger work?
To use Dagger, you call Dagger Functions. Dagger Functions are regular code, written in a supported programming language, and run in containers. Dagger Functions let you encapsulate common operations or workflows into discrete units with clear inputs and outputs.

Dagger Functions are the fundamental unit of computing in Dagger. Core pipeline operations, such as "pull a container image", "copy a file", "forward a TCP port", are exposed as callable Dagger Functions. Dagger also adds a crucial innovation: instead of calling one Dagger Function at a time, callers can chain multiple Dagger Functions together into a dynamic pipeline, with a single call.

The Dagger Engine provides some core functions, but you are encouraged to write your own and share them with others. Dagger also lets you import and reuse Dagger Functions developed by your team, your organization or the broader Dagger community.

See the architecture overview for more information.

How are Dagger Functions used and shared?
The simplest and most common way to use Dagger Functions is via the Dagger CLI. The Dagger CLI is a full-featured, easy to use tool that can be used interactively from a terminal or non-interactively from a shell script or a CI configuration. But Dagger Functions can also be called from other Dagger Functions.

Dagger Functions are packaged, shared and reused using modules. The Daggerverse is a free service run by Dagger, which indexes all publicly available Dagger modules, and lets you easily search and consume them.

Modules don't need to be installed locally. Dagger lets you consume modules from GitHub repositories as well. You call functions from external modules in exactly the same way as you call core functions.
"""
    output = AIMarketing()
    output.getText(scrappedOutput)
    