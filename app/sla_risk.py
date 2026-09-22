class SLARiskModel:
    
    def __init__(self):
        self.model = None

    def load_model(self, model_path):
        # ML model loading, hayet2amel ba3d el training
        pass

    def predict(self, features):
        """
        Rule-based baseline. features dict lazem yekoon fih bas:
        - workload: "Low" | "Medium" | "High"
        - priority: "Low" | "Medium" | "High" | "Critical"
        - ticket_age_hours: float
        Mesh momken tetla3 fi hagat zay resolved_at (leakage).

        Recall-centric: wahed shart bas kefaya, 3ashan
        missing a breaching ticket akhtar men false alarm.
        """
        if self.model is not None:
            # future: ML prediction path
            pass

        workload = features.get("workload", "Low")
        priority = features.get("priority", "Low")
        age_hours = features.get("ticket_age_hours", 0)

        high_workload = workload == "High"
        high_priority = priority in ("High", "Critical")
        is_old = age_hours >= 6

        risk_score = sum([high_workload, high_priority, is_old])

        # Wahed shart bas kefaya (recall-centric), mesh 2 zay 2abl
        sla_risk = risk_score >= 1

        explanation = (
            f"Rule-based SLA risk: workload={workload}, "
            f"priority={priority}, age_hours={age_hours}."
        )

        return {
            "sla_risk": sla_risk,
            "confidence": 0.6,
            "explanation": explanation,
            "method": "rule-based",
        }