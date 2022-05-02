## SaveYourGroceries API Server

### Rest Principles

1. Uniformity

- Identification of resources – The interface must uniquely identify each resource involved in the interaction between the client and the server.
- Manipulation of resources through representations – The resources should have uniform representations in the server response. API consumers should use these representations to modify the resources state in the server.
- Self-descriptive messages – Each resource representation should carry enough information to describe how to process the message. It should also provide information of the additional actions that the client can perform on the resource.
- Hypermedia as the engine of application state – The client should have only the initial URI of the application. The client application should dynamically drive all other resources and interactions with the use of hyperlinks.

2. Client-Server Architecture
   - Client (ex. EatThat! App) has no interaction with database.
3. Stateless (Independent Requests)
   - Requests do not dependent on the response from previous requests.
4. Cacheable
   - https://restfulapi.net/caching/
5. Layered System
   - Database does not have knowledge of the client application and vice versa.
