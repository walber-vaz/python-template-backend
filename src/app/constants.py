from enum import StrEnum

DB_NAMING_CONVENTION = {
    'ix': '%(column_0_label)s_idx',
    'uq': '%(table_name)s_%(column_0_name)s_key',
    'ck': '%(table_name)s_%(constraint_name)s_check',
    'fk': '%(table_name)s_%(column_0_name)s_fkey',
    'pk': '%(table_name)s_pkey',
}


class Environment(StrEnum):
    LOCAL = 'LOCAL'
    STAGING = 'STAGING'
    PRODUCTION = 'PRODUCTION'

    @property
    def is_debug(self):
        return self in {self.LOCAL, self.STAGING}

    @property
    def is_staging(self):
        return self == self.STAGING

    @property
    def is_deployed(self) -> bool:
        return self in {self.STAGING, self.PRODUCTION}
