from modules.policy_loader import load_policies

#BASE_DIR = Path(__file__).resolve().parent.parent
#YAML_FILE = BASE_DIR / "tests" / "fixtures" / "test_policies.yaml"

"""def test_policies():
    with YAML_FILE.open('r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    policies = {}
    for name, config in data["policies"].items():
        policies[name] = Policy(
            name =name,
            enabled=config.get("enabled"),
            severity=config.get("severity"),
            message=config.get("message"),
        )
            
        assert len(policies) > 0
        assert policies["any_any"]
   """      
        
def test_policies():
    policies = load_policies()
    assert len(policies) > 0
    assert "any_any" in policies
    policy = policies["any_any"]
    assert policy.name == "any_any"
    assert policies["any_any"].enabled is True
    assert policies["any_any"].severity == "HIGH"
    assert policies["any_any"].message == "Any-Any rule detected."

    
    
