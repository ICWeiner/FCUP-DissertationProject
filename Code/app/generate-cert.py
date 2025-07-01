import trustme

ca = trustme.CA()
cert = ca.issue_cert("192.168.57.22")

cert.private_key_pem.write_to_path("server.key")
cert.cert_chain_pems[0].write_to_path("server.pem")
ca.cert_pem.write_to_path("client.pem")