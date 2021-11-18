import nonebot
mod_list = [elm.module for elm in nonebot.get_loaded_plugins()]
from pathlib import Path

for module in mod_list:
    if Path(mod.__file__).name in ["__init__.py"]:
            # is a package, search the folder for command/aliases info
            p_dir = Path(mod.__file__).parent
            info = ""
            for file in p_dir.glob("*.py"):
                try:
                    info = extrac_info(file)
                except Exception as e:
                    logger.error("file: %s, extrac_info(file) exc: %s", file, e)
                    info = ""
                if info.strip():
                    break
    else:
        try:
            info = extrac_info(mod.__file__)
        except Exception as e:
            logger.error(
                "mod.__file__: %s, extrac_info(mod.__file__) exc: %s", mod.__file__, e
            )
            info = ""

    info = info.strip()