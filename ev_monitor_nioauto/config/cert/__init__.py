import os

cert_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cert")
base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

default_ca_chain = os.sep.join([cert_dir, "default_cert", "ca", "tls_tsp_trustchain.pem"])
alps_in_ca_chain = os.sep.join([cert_dir, "web_tsp_alps_test", "tsp-alps-test-in.trustchain"])

web_chain = os.sep.join([cert_dir, "web_tsp-test-int", "web_tsp-test-int.trustchain"])
web_cert = (os.sep.join([cert_dir, "web_tsp-test-int", "web_tsp-test-int.cert"]),
            os.sep.join([cert_dir, "web_tsp-test-int", "web_tsp-test-int.key"]))
web_cert_mp = (os.sep.join([cert_dir, "web_tsp-stg-eu", "web_tsp-stg-eu.cert"]),
               os.sep.join([cert_dir, "web_tsp-stg-eu", "web_tsp-stg-eu.key"]))

web_cert_alps = (os.sep.join([cert_dir, "web_tsp_alps_test", "tsp-alps-test-in.cert"]),
                 os.sep.join([cert_dir, "web_tsp_alps_test", "tsp-alps-test-in.key"]))

v_cert = (os.sep.join([base_dir, "test", "ChA-0A48kgj5023-0Fc0MEB8EAEYlgkglU4oAg==", "client", "tls_lion_cert.pem"]),
               os.sep.join([base_dir, "test", "ChA-0A48kgj5023-0Fc0MEB8EAEYlgkglU4oAg==", "client", "tls_lion_priv_key.pem"]))

