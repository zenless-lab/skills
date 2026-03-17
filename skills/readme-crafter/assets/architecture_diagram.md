## 🏗 Architecture

Here is a high-level overview of the system architecture.

```mermaid
graph TD
    Client[Client App/Browser] -->|HTTP/REST| API[API Gateway]
    API --> Auth[Auth Service]
    API --> Core[Core Business Service]
    Core --> DB[(PostgreSQL)]
    Core --> Cache[(Redis Cache)]

    subgraph Background Processing
        Core -->|Publishes Events| Queue[Message Queue]
        Queue --> Worker[Worker Node]
        Worker --> ThirdParty[External Services]
    end
```

_This diagram is generated using Mermaid.js. It allows developers to update the architecture directly in the markdown file._
