from app.blueprints.movies import movies as movies_blueprint
from app.blueprints.nominations import nominations as nominations_blueprint
from app.blueprints.userNominations import userNominations as userNominations_blueprint
from app.blueprints.proxy import proxy as proxy_blueprint
from app.blueprints.category import categories as categories_blueprint
from app.blueprints.auth import auth as auth_blueprint

blueprints = [movies_blueprint, nominations_blueprint, userNominations_blueprint, categories_blueprint, proxy_blueprint, auth_blueprint]