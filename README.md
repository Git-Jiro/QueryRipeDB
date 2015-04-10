# QueryRipeDB
## Get the sub net of an IP address from the Ripe database

This script fetches IP addresses from STDIN and outputs subnets in CIDR notation on STDOUT.

### Related documentation
- https://github.com/RIPE-NCC/whois/wiki/WHOIS-REST-API
- https://www.ripe.net/data-tools/support/documentation/ripe-database-documentation-1.78

### TODO
 - For some IP addresses, there are no route objects in the Ripe DB.
   In this case the script should derive a subnetmask from INETNUM objects.
 - Provide tests.
