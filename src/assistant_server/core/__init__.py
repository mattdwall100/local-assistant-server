"""Core app primitives such as settings."""
# global infra concerns
# logging belongs in core, since it's a cross-cutting concern that is used throughout the application, and we want to have a centralized place to configure it. By setting up logging in the core module, we can ensure that all parts of the application use a consistent logging configuration, and we can easily manage log levels, formats, and handlers from a single location. This also allows us to avoid having to configure logging separately in each module, which can lead to duplication and inconsistencies.
# We can set up a logger in the core module, and then import and use that logger in other parts of the application as needed. This way, we can have a unified logging strategy across
