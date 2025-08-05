**On agency (WIP)**

The AI boom began in earnest in December 2022 with the release of ChatGPT.

Since then, "agent" and "agentic" have become very fashionable buzzwords. I used to roll my eyes whenever I saw these terms --- seeing it as an empty marketing modifier --- but recently I noticed that, at least among legitimate projects, there is a correlation between use of these terms and demonstrations or referenfces to <b>tool use</b>.

Upon further examination I realized that I had internalized the notion of agent from reinforcement learning. That is, an agent is a thing which interacts with its environment by performing actions (after which it receives rewards). Let's consider the immediate "environment" of, say, a command line interface for having conversations with a large language model. Most broadly, its environment is the "digital universe", by which I mean essentially the memory of the set of all interconnected devices. (We could regard the contents of my monitor as included in this because, for example, before a frame is rendered to my screen it exists in buffers in the memory of my graphics card.)

For a vanilla chat bot, the extent to which it can interact with its environment is painfully limited to renderiung text on a screen that might be read by a user. If we try to formalize the notion of "degree of agency" as extent of interaction with or degree of influence over the environment, then this vanilla chatbot has almost no agency whatsoever.

However, as we start to add tools --- a tool to execute shell commands, a tool to send HTTP requests, tools to create and edit files, tools to spawn new instances --- the degree of agenccy begins to markedly increase. In the limit, such digital "agents" employing such tools could hypothetically discover zero-days and thereby obtain access to <i>all</i> interconnected devices.

And such an agent could also, hypothetically, become arbitrarily intelligent, so that it could induce humans or other physical agents to manipulate the physical universe directly. In this sense, the digital agent's environment is not just the "digital univertse" but actually the physical universe. So perhaps Agent Smith was right after all and digital agents really aren't so different from physical ones like you and I.