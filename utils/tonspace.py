from pytonapi.schema.nft import NftItems
from pytonapi import Tonapi

from config.config import Config, load_config
from database import t_users, t_mining


class TonSpace:
    config: Config = load_config()
    TON: Tonapi = Tonapi(api_key=config.secrets.ton_api)
    address: str = "UQA0IvXBnVMRI9BqM8GK-KeMPam7QBhAyiPAdfJUQ-Zzx_rk"
    available: list[str] = ["BRONZE INCH", "SILVER INCH", "GOLD INCH", "BLACK INCH", "GECKOSHI INCH", "GHOSTEX INCH"]

    @classmethod
    async def balance(cls) -> float:
        balance: float = cls.TON.accounts.get_info(cls.address).balance.to_amount()
        return balance

    @classmethod
    def nft(cls, user_id: int) -> NftItems:
        wallet: str = t_users.select(("wallet", ), "user_id", user_id)
        nft: NftItems = cls.TON.accounts.get_nfts(account_id=wallet)
        return nft

    @classmethod
    def filter_nft(cls, nft_items: NftItems) -> list:
        inch_nft: list = []
        for nft in nft_items.nft_items:
            try:
                name: str = nft.metadata["name"]
            except:
                pass
            else:
                if name in cls.available:
                    inch_nft.append(nft)
        return inch_nft

    @classmethod
    def booster(cls, user_id: int, booster: float = 1) -> float:
        nfts: list = cls.filter_nft(cls.nft(user_id))
        for nft in nfts:
            for attr in nft.metadata["attributes"]:
                if attr["trait_type"] == "multiplier":
                    booster = booster * float(attr["value"])
        print(booster)
        t_mining.assign("booster", booster, "user_id", user_id)
        return round(booster, 2)
