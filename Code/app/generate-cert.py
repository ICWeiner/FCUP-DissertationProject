import trustme

ca = trustme.CA()

fastapi_cert = ca.issue_cert("localhost", "192.168.57.164")
fastapi_cert.private_key_pem.write_to_path("fastapi.key")
fastapi_cert.cert_chain_pems[0].write_to_path("fastapi.pem")

cert = ca.issue_cert("192.168.57.22")
cert.private_key_pem.write_to_path("pve.key")
cert.cert_chain_pems[0].write_to_path("pve.pem")

ca.cert_pem.write_to_path("client.pem")