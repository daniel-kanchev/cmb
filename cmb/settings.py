LOG_LEVEL = 'WARNING'
BOT_NAME = 'cmb'
SPIDER_MODULES = ['cmb.spiders']
NEWSPIDER_MODULE = 'cmb.spiders'
ROBOTSTXT_OBEY = True
ITEM_PIPELINES = {
   'cmb.pipelines.DatabasePipeline': 300,
}