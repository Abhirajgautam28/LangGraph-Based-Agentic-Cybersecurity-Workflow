def is_in_scope(target, allowed_scopes):
    """
    Check if target is within any of the allowed scopes.
    allowed_scopes: comma-separated string, e.g., "google.com,.example.com,192.168.1.0/24"
    """
    scopes = [s.strip() for s in allowed_scopes.split(",")]
    for scope in scopes:
        # Simple check: if target ends with allowed scope or exactly matches it
        if target.endswith(scope) or target == scope:
            return True
    return False

if __name__ == "__main__":
    allowed = "google.com,.example.com,192.168.1.0/24"
    targets = ["mail.google.com", "test.example.com", "evil.com"]
    for t in targets:
        print(f"{t}: {is_in_scope(t, allowed)}")
