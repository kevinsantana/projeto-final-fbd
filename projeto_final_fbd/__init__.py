from loguru import logger


logger.add("etl.log", colorize=True, serialize=True)
logger.remove(0)

logger.level("NOME RESPONSAVEL", no=38, color="<yellow>")
logger.level("NOME BENEFICIARIO", no=39, color="<green>")
logger.level("BENEFICIARIO", no=500, color="<red>")
logger.level("CODIGO MUNICIPIO", no=40, color="<blue>")