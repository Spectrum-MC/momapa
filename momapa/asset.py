from typing import Optional, Self


class AssetIndex:
    id: str = None
    hash: str = None
    size: int = None
    total_size: int = None
    url: str = None

    @staticmethod
    def parse(data: dict) -> Optional[Self]:
        if not data:
            return None

        assets = AssetIndex()
        assets.id = data.get('id')
        assets.hash = data.get('sha1')
        assets.size = data.get('size')
        assets.total_size = data.get('totalSize')
        assets.url = data.get('url')

        return assets
