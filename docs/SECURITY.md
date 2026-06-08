# Security

## Current package

This launch kit uses no external Python dependencies. The static verifier runs in the browser. The local API server is for development and local demos.

## Security boundary

Do not expose the included development API server directly to the public internet without production hardening.

## Recommended production hardening

- authentication;
- TLS;
- request size limits;
- rate limiting;
- audit logging;
- database backups;
- signed receipt storage;
- secret management;
- separation of public and private vaults.
