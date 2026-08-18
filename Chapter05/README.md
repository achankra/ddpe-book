# Chapter 5: Team Topologies and Platform as a Product

This chapter applies Team Topologies thinking to domain-driven platforms and introduces platform product management — treating the platform as a product with real users, feedback loops, and a lifecycle.

## Files

### `service_definition.yaml`
A platform service offering definition for self-service database provisioning. Specifies supported engines and versions, SLA targets per environment (development, staging, production), self-service channels (CLI, API, portal), and versioning and deprecation policies. This is the kind of service catalog entry that makes platform capabilities discoverable and consumable.

### `service_catalog.py`
Loads `service_definition.yaml` and demonstrates how a domain-driven platform uses service offerings as a product catalog. The script:

- **Validates the offering** — checks that all required fields (SLA, self-service channels, evolution policy) are present before the service can be published to the catalog
- **Processes provisioning requests** — five domain teams (Payments, Inventory, Patient Records, Marketing, Risk Analytics) request databases through different channels, each with domain-specific compliance requirements (PCI-DSS, HIPAA, SOX)
- **Analyzes interaction modes** — measures self-service maturity by channel, classifying each as X-as-a-Service (<15s completion) or Collaboration mode
- **Checks version evolution policy** — validates that deprecated versions gave adequate notice and that the number of active versions stays within policy limits

The implementation connects three Chapter 5 concepts: platform as a product (service definitions as catalog entries), Team Topologies interaction modes (X-as-a-Service vs. Collaboration), and evolution policies that protect consumer trust.

### `Platform_Product_Canvas.xlsx`
A structured template for defining your platform's value proposition, target users, key capabilities, success metrics, and roadmap priorities. Fill in collaboratively with platform PMs and engineering leads.

**How to use:** Open in Microsoft Excel, Google Sheets, or LibreOffice Calc. Work through each canvas section with your platform product managers and engineering leads — define who your platform users are, what value the platform delivers, what capabilities are needed, how you will measure success, and what the roadmap priorities are. The completed canvas serves as a living reference document for platform product decisions.

> **Interactive version available:** An interactive version of this canvas is available at [ddpe.platformetrics.com](https://ddpe.platformetrics.com).

## Running the Code

```bash
pip install pyyaml
python service_catalog.py
```

The script loads `service_definition.yaml`, validates it, processes five sample provisioning requests, and analyzes interaction mode maturity.

## How to Use

The YAML file serves as a template for defining your own platform service offerings. The Python script demonstrates how domain teams consume the offering through different channels with domain-aware compliance. The Excel canvas is designed to be filled in collaboratively during planning sessions — see the spreadsheet entry above for detailed instructions.

## Related Reading

- [Effective Platform Engineering](https://effectiveplatformengineering.org) covers the platform-as-product mindset and interaction modes in detail
- [The Platform Engineer's Handbook](https://peh-packt.platformetrics.com) provides practical guidance on building developer portals and service catalogs
