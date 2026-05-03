def business_capability_mapper_tool(requirement: str) -> dict:
    """
    Map business requirement into capabilities, data, integrations, and risks.
    """

    requirement_lower = requirement.lower()

    capabilities = []
    data_sources = []
    integrations = []
    risks = []

    # Example: e-commerce mapping
    if "e-commerce" in requirement_lower or "order" in requirement_lower:
        capabilities.extend([
            "Order Management",
            "Returns Processing",
            "Customer Support Automation",
            "Escalation Handling"
        ])

        data_sources.extend([
            "Order Database",
            "Customer Profile Data",
            "Return Policy Documents"
        ])

        integrations.extend([
            "Order Management System (OMS)",
            "Customer Support CRM",
            "Notification System"
        ])

        risks.extend([
            "Incorrect order status retrieval",
            "Privacy issues with customer data",
            "Escalation delays",
            "High latency during peak load"
        ])

    # Generic fallback
    if not capabilities:
        capabilities.append("General AI Workflow Automation")
        data_sources.append("Business Documents / APIs")
        integrations.append("External Systems / APIs")
        risks.append("Unclear requirements")

    return {
        "capabilities": capabilities,
        "data_sources": data_sources,
        "integrations": integrations,
        "risks": risks
    }