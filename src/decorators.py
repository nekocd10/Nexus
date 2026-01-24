"""
Nexus Backend Decorator System
Handles @route, @model, @middleware, @auth, etc. for .nxsjs files
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from enum import Enum

class DecoratorType(Enum):
    """All supported Nexus decorators for backends"""
    # Application & Environment
    CONFIG = "config"
    ENV = "env"
    PROFILE = "profile"
    FEATURE = "feature"
    FLAG = "flag"
    
    # Lifecycle & Execution
    STARTUP = "startup"
    SHUTDOWN = "shutdown"
    TASK = "task"
    CRON = "cron"
    WORKER = "worker"
    QUEUE = "queue"
    
    # Data & State
    MODEL = "model"
    REPOSITORY = "repository"
    TRANSACTION = "transaction"
    CACHE = "cache"
    INDEX = "index"
    MIGRATION = "migration"
    SEED = "seed"
    
    # Security
    AUTH = "auth"
    PERMISSION = "permission"
    ROLE = "role"
    POLICY = "policy"
    RATELIMIT = "ratelimit"
    CORS = "cors"
    CSRF = "csrf"
    
    # Validation & Contracts
    VALIDATE = "validate"
    SCHEMA = "schema"
    CONTRACT = "contract"
    SANITIZE = "sanitize"
    
    # Observability
    LOG = "log"
    TRACE = "trace"
    METRIC = "metric"
    HEALTH = "health"
    AUDIT = "audit"
    
    # Performance & Scaling
    OPTIMIZE = "optimize"
    PARALLEL = "parallel"
    CLUSTER = "cluster"
    SHARD = "shard"
    LOADBALANCE = "loadbalance"
    
    # Error Handling & Resilience
    ERROR = "error"
    RETRY = "retry"
    FALLBACK = "fallback"
    TIMEOUT = "timeout"
    CIRCUITBREAKER = "circuitbreaker"
    
    # Modularity & Architecture
    MODULE = "module"
    SERVICE = "service"
    PLUGIN = "plugin"
    EXTENSION = "extension"
    BOUNDARY = "boundary"
    
    # Realtime & Networking
    SOCKET = "socket"
    STREAM = "stream"
    EVENT = "event"
    PUBSUB = "pubsub"
    CHANNEL = "channel"
    
    # Files & Media
    UPLOAD = "upload"
    FILE = "file"
    MEDIA = "media"
    CDN = "cdn"
    
    # Testing & Quality
    TEST = "test"
    MOCK = "mock"
    BENCHMARK = "benchmark"
    ASSERT = "assert"
    
    # Deployment & Infrastructure
    DEPLOY = "deploy"
    REGION = "region"
    RESOURCE = "resource"
    LIMIT = "limit"
    
    # HTTP Routes
    ROUTE = "route"
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"
    PATCH = "patch"
    HEAD = "head"
    OPTIONS = "options"


@dataclass
class DecoratorConfig:
    """Configuration for a decorator"""
    type: DecoratorType
    args: List[Any] = field(default_factory=list)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    
    def __repr__(self):
        args_str = ", ".join(str(a) for a in self.args)
        kwargs_str = ", ".join(f"{k}={v}" for k, v in self.kwargs.items())
        all_args = ", ".join(filter(None, [args_str, kwargs_str]))
        return f"@{self.type.value} {all_args}" if all_args else f"@{self.type.value}"


@dataclass
class BackendRoute:
    """HTTP Route definition"""
    method: str  # GET, POST, PUT, DELETE, PATCH
    path: str
    handlers: List[str] = field(default_factory=list)
    middleware: List[str] = field(default_factory=list)
    auth_required: bool = False
    rate_limited: bool = False
    cache_enabled: bool = False
    validation_schema: Optional[Dict] = None
    response_schema: Optional[Dict] = None
    timeout_ms: int = 30000
    retry_count: int = 0
    
    def __repr__(self):
        return f"@route {self.method} {self.path}"


@dataclass
class BackendModel:
    """Data model definition"""
    name: str
    fields: Dict[str, str]  # field_name -> type
    indexes: List[str] = field(default_factory=list)
    validations: Dict[str, List[str]] = field(default_factory=dict)
    hooks: Dict[str, List[str]] = field(default_factory=dict)  # before_save, after_save, etc.
    
    def __repr__(self):
        return f"@model {self.name}"


@dataclass
class BackendMiddleware:
    """Middleware definition"""
    name: str
    handler: str
    order: int = 0
    applies_to: List[str] = field(default_factory=list)  # routes it applies to
    
    def __repr__(self):
        return f"@middleware {self.name}"


@dataclass
class BackendService:
    """Service definition"""
    name: str
    methods: Dict[str, Callable] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    
    def __repr__(self):
        return f"@service {self.name}"


@dataclass
class BackendTask:
    """Background task definition"""
    name: str
    handler: str
    schedule: Optional[str] = None  # cron expression
    queue: str = "default"
    retry: int = 3
    timeout_ms: int = 60000
    
    def __repr__(self):
        return f"@task {self.name}"


@dataclass
class BackendConfig:
    """Application configuration"""
    port: int = 5000
    host: str = "0.0.0.0"
    database: Optional[str] = None
    redis: Optional[str] = None
    log_level: str = "info"
    environment: str = "development"
    debug: bool = False
    cors_enabled: bool = False
    cors_origins: List[str] = field(default_factory=list)
    rate_limit_enabled: bool = False
    rate_limit_requests: int = 100
    rate_limit_window_ms: int = 60000
    
    def __repr__(self):
        return "@config"


class BackendRegistry:
    """Registry for all backend decorators and their handlers"""
    
    def __init__(self):
        self.routes: Dict[str, BackendRoute] = {}
        self.models: Dict[str, BackendModel] = {}
        self.middleware: Dict[str, BackendMiddleware] = {}
        self.services: Dict[str, BackendService] = {}
        self.tasks: Dict[str, BackendTask] = {}
        self.config: BackendConfig = BackendConfig()
        self.decorators: List[DecoratorConfig] = []
    
    def register_route(self, route: BackendRoute):
        """Register an HTTP route"""
        key = f"{route.method}:{route.path}"
        self.routes[key] = route
        return route
    
    def register_model(self, model: BackendModel):
        """Register a data model"""
        self.models[model.name] = model
        return model
    
    def register_middleware(self, middleware: BackendMiddleware):
        """Register middleware"""
        self.middleware[middleware.name] = middleware
        return middleware
    
    def register_service(self, service: BackendService):
        """Register a service"""
        self.services[service.name] = service
        return service
    
    def register_task(self, task: BackendTask):
        """Register a background task"""
        self.tasks[task.name] = task
        return task
    
    def set_config(self, config: BackendConfig):
        """Set application configuration"""
        self.config = config
        return config
    
    def register_decorator(self, decorator: DecoratorConfig):
        """Register a generic decorator"""
        self.decorators.append(decorator)
        return decorator
    
    def get_all_routes(self) -> Dict[str, BackendRoute]:
        """Get all registered routes"""
        return self.routes.copy()
    
    def get_all_models(self) -> Dict[str, BackendModel]:
        """Get all registered models"""
        return self.models.copy()
    
    def get_route(self, method: str, path: str) -> Optional[BackendRoute]:
        """Get a specific route"""
        key = f"{method}:{path}"
        return self.routes.get(key)
    
    def get_model(self, name: str) -> Optional[BackendModel]:
        """Get a specific model"""
        return self.models.get(name)
    
    def summary(self) -> Dict:
        """Get a summary of all registered items"""
        return {
            "routes": len(self.routes),
            "models": len(self.models),
            "middleware": len(self.middleware),
            "services": len(self.services),
            "tasks": len(self.tasks),
            "decorators": len(self.decorators),
            "config": vars(self.config)
        }
    
    def __repr__(self):
        return f"BackendRegistry(routes={len(self.routes)}, models={len(self.models)}, middleware={len(self.middleware)})"


# Global backend registry instance
backend_registry = BackendRegistry()


def get_backend_registry() -> BackendRegistry:
    """Get the global backend registry"""
    return backend_registry
