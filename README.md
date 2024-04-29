# **Metric Internship Task N2**

## **Description:**
#### You are working in a startup whose product is growing quite fast recently. Based on the success, the CEO decided to start fundraising from Venture Capital firms. But to do that, he asked you to first create a database of VCs that he can then reach out to.  Your task is to build a Generative AI assistant for the CEO, which will be able to assess VC similarity and perform information extraction.

#### Given VC website URL as an input by the user, your Generative AI assistant should be able to:
- Scrape Home page of the website and store the content in vectorDB of your choice,
- Extract the following information and show it to the user as a JSON object: VC name, contacts, industries that they invest in, investment rounds that they participate/lead.
- Compare VC website content to the other VC website contents in the database (some examples provided below) and print the 3 most similar VCs.

## **Technical Requirements:**
- Build the Generative AI assistant (e.g. using OpenAI APIs),
- Build an API (using FastAPI/Flask) that can be used as an interface for the AI Assistant,
- Either host the vectorDB, and the assistant app on cloud or containerize using Docker,
- Submit GitHub URL with your codebase. If the app is deployed in the cloud, submit the app URL as well.

## **Evaluation criteria:**
- Completeness of your work,
- Quality of the assistant both for information extraction as well as similarity,
- Quality of code,
- Architectural and Software Choices.

#### Example VC websites that you can populate the database initially to compute the similarity:
- www.accel.com
- www.a16z.com
- www.greylock.com
- www.benchmark.com
- www.sequoiacap.com
- www.indexventures.com
- www.kpcb.com
- www.lsvp.com
- www.matrixpartners.com
- www.500.co
- www.sparkcapital.com
- www.insightpartners.com


