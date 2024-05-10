from typing import Optional, Self


class JavaVersion:
    component: str = None
    major_version: int = None

    @staticmethod
    def parse(data: dict) -> Optional[Self]:
        if not data:
            return None

        jv = JavaVersion()

        jv.component = data.get('component')
        jv.major_version = data.get('majorVersion')

        return jv
