from app.utils.app_request_parser import AppRequestParser


general_parser = AppRequestParser(bundle_errors=True)
general_parser.add_argument("page", help="Current Page", location="args", type=int)
general_parser.add_argument("per_page", help="Data Per Page", location="args", type=int)
