# FDC3 Standard

FDC3 (Financial Desktop Connectivity and Collaboration Consortium) 2.2 defines specific naming conventions for both intents and context data types to ensure interoperability and standardization across financial desktop applications. Understanding these naming formats is essential for developers building FDC3-compliant applications and integrations.

## Intent Naming Format in FDC3 2.2

Intents in FDC3 represent standardized verbs that define actions that one application can request from another. The naming convention for intents follows specific guidelines to ensure consistency and discoverability across the FDC3 ecosystem.

### General Naming Guidelines

Intent names in FDC3 2.2 should adhere to the following fundamental rules:

**Character Requirements**: Intent names should be free of non-alphanumeric characters, with the exception of the dot character (.) which is used for namespacing purposes. This restriction ensures that intent names remain machine-readable and avoid parsing issues across different systems and programming languages.

**Casing Convention**: All intent names must use UpperCamelCase format. This means each word in the intent name begins with a capital letter, with no spaces or underscores between words. For example, `ViewChart` or `CreateOrder` follow this convention correctly.

**Semantic Clarity**: Intent names should be recognizable and self-evident in terms of what action they represent. The name should clearly communicate the expected behavior without requiring extensive documentation lookup.

### Intent Name Prefixes and Categories

FDC3 2.2 organizes intents into different categories based on their functional purpose, and these categories are distinguished through specific prefixes:

**UI-Focused Intents (Original Set)**: These intents primarily concern the display of content to users or initiation of interactions:

- **View___** prefix: Indicates that content should be displayed to the user. Examples include `ViewChart`, `ViewContact`, and `ViewInstrument`. The expected behavior is that the receiving application will present the provided context data in a user-facing manner.
- **Start___** prefix: Indicates that an interaction should be initiated. Examples include `StartChat` or `StartEmail`. These intents trigger the creation of new interaction sessions such as chat rooms, email composition windows, or similar communication channels.

**CRUD Operation Intents (Added in FDC3 2.0)**: These intents provide standardized operations for Create, Read, Update, and Delete functionality:

- **Create___** prefix: Indicates that a new record or entity should be created. This operation will fail if the entity already exists. Examples include `CreateOrder`, `CreateContact`, and `CreateInstrument`.
- **Update___** prefix: Indicates that an existing record or entity should be updated. This operation will fail if the entity does not exist. Examples include `UpdateOrder`, `UpdatePosition`, and `UpdatePortfolio`.
- **CreateOrUpdate___** prefix: Indicates that a new record should be created or an existing one updated if it already exists. This provides flexibility for idempotent operations.
- **Delete___** prefix: Indicates that an existing record or entity should be deleted. This operation will fail if the entity does not exist.
- **Get___** prefix: Indicates that a record or entity should be retrieved and returned as an intent result. This operation will fail if the record does not exist.
- **Share___** prefix: Indicates that a record or entity should be shared with other applications or users. This operation will fail if the entity does not exist.

### Namespacing Convention

FDC3 reserves all standard intent names that do not contain a namespace prefix for its own use. Applications may define their own proprietary intents, but these should be namespaced to avoid collision with other applications or future standard intents.

**Standard Intents**: These are reserved for FDC3 and follow the naming pattern without any namespace prefix, such as `ViewChart` or `CreateOrder`.

**Proprietary Intents**: Applications should namespace their proprietary intents using their application name or organization name to avoid conflicts. The convention is to use the format `applicationName.IntentName` or `organizationName.IntentName`. For example, if an application named "myChart" defines a proprietary intent for a specialized chart viewing behavior, it should be named `myChart.Foo` rather than simply `Foo`.

This namespacing approach ensures that proprietary intents remain distinct from standard FDC3 intents and from intents defined by other applications, reducing the likelihood of naming collisions in complex desktop environments.

## Context Naming Format in FDC3 2.2

Context data in FDC3 represents the "nouns" that accompany intents, carrying the actual data payload for the requested action. The context system uses a type-based approach where each context object must declare its type through a specific naming convention.

### The Type Property (Required)

The `type` property is the only required element in the FDC3 context data schema. This property serves multiple critical functions:

**Data Identification**: The type property identifies what type of data the context object represents and defines its shape or structure. This identification enables the FDC3 API to route context data appropriately to applications that can handle that specific type.

**Intent Discovery and Routing**: The type property is used in conjunction with intent discovery and routing through FDC3 App Directories. Applications declare which context types they can handle for specific intents, enabling the desktop agent to make intelligent routing decisions.

**Data Contract Definition**: The type establishes the basic contract or "shape" for all data exchanged by FDC3 operations, ensuring that sending and receiving applications have a shared understanding of the data structure.

### Namespace Convention for Context Types

FDC3 2.2 uses a namespaced approach for context type names to distinguish between standardized types and custom types:

**Standardized FDC3 Context Types**: All standard context types defined by FDC3 are prefixed with the `fdc3` namespace. This creates a clear distinction between types that are part of the standard and those that are custom implementations. Examples of standardized context types include:

- `fdc3.contact` - Represents a single contact entity
- `fdc3.contactList` - Represents a list of contacts
- `fdc3.country` - Represents a country identifier
- `fdc3.instrument` - Represents a financial instrument
- `fdc3.instrumentList` - Represents a list of financial instruments
- `fdc3.organization` - Represents an organization entity
- `fdc3.position` - Represents a position or holding
- `fdc3.portfolio` - Represents a portfolio of positions

**Non-Standard (Custom) Types**: Organizations can define their own context types for specialized use cases not covered by the standard. These custom types should use an organization-specific namespace prefix. For example, an asset management company named BlackRock might define a custom context type as `blackrock.fund` for representing fund-specific data.

This namespacing convention ensures that custom types remain distinct from standard types and from types defined by other organizations, preventing naming conflicts and enabling clear identification of data provenance.

### Context Data Schema Structure

All context types in FDC3 2.2 share a common base structure with the following properties:

| Property | Type | Required | Purpose |
| --- | --- | --- | --- |
| `type` | string | **Yes** | Identifies the data type and shape of the context object |
| `name` | string | No | Provides a display name or additional descriptive information |
| `id` | object | No | Contains key-value pairs for identifying the entity (e.g., ISIN, CUSIP, Bloomberg ID) |

The `id` property is optional at the base level, though some derived types may require at least one identifier. Applications can and should provide multiple equivalent identifiers (such as ISIN, CUSIP, and Bloomberg ticker) to aid cross-platform identification and ensure that receiving applications can match the context data to their internal records regardless of which identifier system they use.

### Key Principles for Context Naming

**Extensibility**: Context types can be extended with custom fields as appropriate for specific use cases, while maintaining the required base structure defined by the type system.

**Minimum Required Fields**: Context types define minimum required fields that all implementations must support, but implementations may include additional fields as needed.

**Backward Compatibility**: Existing context types maintain compatibility across versions, ensuring that applications built against older versions of the standard continue to work with newer implementations.

**Discoverability**: The namespaced format enables clear identification of context types and their provenance, supporting discoverability through FDC3 App Directories and desktop agents.

## Compliance and Best Practices

For applications to be considered FDC3 2.2 compliant, they must adhere to specific requirements regarding intent and context naming:

**Intent Compliance**: Applications MUST meet the expected context and behavior defined for any FDC3-defined standard intents they implement. They SHOULD prefer FDC3-defined standard intents over proprietary intents when available for their use case. When proprietary intents are necessary, they SHOULD follow the recommended naming conventions and apply namespacing to avoid collision. Intent listeners SHOULD be set up within 15 seconds of application launch to ensure responsive intent resolution.

**Context Compliance**: Applications MUST use the correct `type` property values when sending context data and MUST handle the context types they declare support for in their application metadata. When defining custom context types, applications SHOULD use organization-specific namespaces to avoid conflicts with standard types or types from other organizations.

This comprehensive naming framework ensures that FDC3 2.2 implementations can interoperate effectively while maintaining flexibility for organization-specific requirements and future extensibility of the standard.

# Portal Intent Format

All intent in Portal should be start with "scb.fmptp".

For example, if user want to view cashflows in cashflow blotter, then they can raise the intent "scb.fmptp.ViewCashflows".

# Portal Context Format

All context type in Portal should be start with "scb.fmptp".

For example, if user want to view cashflows in cashflow blotter, they can raise intent with context "scb.fmptp.cashflows".

```js
{
  "type": "scb.fmptp.cashflows",
  "id": {
    "tradeId": "6952326346"
  }
}
```