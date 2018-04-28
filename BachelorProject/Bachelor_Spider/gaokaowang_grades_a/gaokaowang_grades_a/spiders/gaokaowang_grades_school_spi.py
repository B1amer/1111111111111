import scrapy, re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from gaokaowang_grades_a.items import GaokaowangItem_school_scoreline


class GaokaowangGradesSpiSpider(CrawlSpider):
    name = 'gaokaowang_grades_school_spi'
    allowed_domains = ['college.gaokao.com']
    start_urls = ['http://college.gaokao.com/schpoint/']

    rules = (
        Rule(
            LinkExtractor(allow=(
                                'schpoint/a\d+/p\d+',
                                #  'schpoint/a\d+',
                                 # 'schpoint/a\d+/b\d+',
                                 ),
                          deny=('areapoint/a\d+/s',
                                'areapoint/a\d+/y',
                                'schpoint/a\d+/b\d+/y',
                                'schpoint/a\d+/b\d+/s',
                                'schpoint/a\d+/p\d+/y',
                                'schpoint/a\d+/p\d+/s',
                                ),
                          ),
            follow = True,
        ),
        Rule(LinkExtractor(allow=('school/tinfo/\d+/result/\d+/1')),
            callback = 'parse_item_like',
        )
    )

    def parse_item_like(self, response):
        # first_year_depend_pre = response.xpath("//tr[@class='szw'][1]/td[1]/text").extract()
        # line_frame = response.xpath(r"//tr[@class='szw']/td[1]|//tr[@class='sz']/td[1]").extract()
        line_1_frame = response.xpath(r"//tr[@class='szw']/td[1]").extract()
        line_2_frame_pre = response.xpath(r"//tr[@class='sz']/td[1]").extract()

        #如果有一行以上
        if line_1_frame:
            for i, line in enumerate(line_1_frame):
                #有多行
                if line_2_frame_pre:

                    school_item_like = self.get_item()

                    #算出偶数行的行数
                    line_2_counts = len(response.xpath(r"//tr[@class='sz']").extract())

                    #奇数行用szw匹配
                    if response.xpath(r"//div[@id='wrapper']/div[@class='cont_l in']/p[@class='btnFsxBox']/font[1]/text()").extract():
                        school_item_like['school_name'] = response.xpath(r"//div[@id='wrapper']/div[@class='cont_l in']/p[@class='btnFsxBox']/font[1]/text()").extract()[0]

                    if response.xpath(r"//div[@class='cont_l in']/p[@class='btnFsxBox']/font[2]/text()").extract():
                        school_item_like['location_name'] = response.xpath(r"//div[@class='cont_l in']/p[@class='btnFsxBox']/font[2]/text()").extract()[0]

                    re_rule_1 = ("//tr[@class='szw'][{a}]/td[1]/text()".format(a = i + 1))
                    if response.xpath(re_rule_1).extract():
                        year_icon = response.xpath(re_rule_1).extract()[0]
                        year_icon_list_1 = []
                        year_icon_list_1.append(year_icon)

                    # 只取2010年以上的数据
                        if int(year_icon) >= 2010:

                            if response.xpath(r"//tr[@class='szw'][{a}]/td[2]/text()".format(a = i + 1)).extract():
                                school_item_like['lowest_score_{a}_like_l{b}'.format(a = year_icon,b = 1)] = \
                                response.xpath(r"//tr[@class='szw'][{a}]/td[2]/text()".format(a = i + 1)).extract()[0]

                            if response.xpath(r"//tr[@class='szw'][{a}]/td[3]/text()".format(a = i + 1)).extract():
                                school_item_like['highest_score_{a}_like'.format(a = year_icon)] = \
                                response.xpath(r"//tr[@class='szw'][{a}]/td[3]/text()".format(a = i + 1)).extract()[0]

                            if response.xpath(r"//tr[@class='szw'][{a}]/td[4]/text()".format(a = i + 1)).extract():
                                school_item_like['average_score_{a}_like'.format(a = year_icon)] = \
                                response.xpath(r"//tr[@class='szw'][{a}]/td[4]/text()".format(a = i + 1)).extract()[0]

                            if response.xpath(r"//tr[@class='szw'][{a}]/td[5]/text()".format(a=i + 1)).extract():
                                school_item_like['admit_people_counts_{a}_like'.format(a = year_icon)] = \
                                response.xpath(r"//tr[@class='szw'][{a}]/td[5]/text()".format(a = i + 1)).extract()[0]

                            if response.xpath(r"//tr[@class='szw'][{a}]/td[6]/text()".format(a=i + 1)).extract():
                                school_item_like['admit_batch_{a}_like'.format(a = year_icon)] = \
                                response.xpath(r"//tr[@class='szw'][{a}]/td[6]/text()".format(a = i + 1)).extract()[0]

                        # the1_line_year =  response.xpath(r"//tr[@class='szw'][1]/td[1]/text()").extract()[0]
                        # the2_line_year =  response.xpath(r"//tr[@class='szw'][1]/td[1]/text()").extract()[0]
                        # the1_line_year =  response.xpath(r"//tr[@class='szw'][1]/td[1]/text()").extract()

                        #偶数行用sz匹配
                        if i <= line_2_counts:
                            re_rule_2 = ("//tr[@class='sz'][{}]/td[1]/text()".format(i + 1))
                            if response.xpath(re_rule_2).extract():
                                year_icon2 = response.xpath(re_rule_2).extract()[0]
                            #只取2010年以上的数据

                            a_for_git = 'asdasd'
                            a_for_git = 'asdasd'
                            a_for_git = 'asdasd'
                            a_for_git = 'asdasd'
                            a_for_git = 'asdasd'
                            if int(year_icon2) >= 2010:

                                if response.xpath(r"//tr[@class='sz'][{a}]/td[2]/text()".format(a = i + 1)).extract():
                                    school_item_like['lowest_score_{a}_like'.format(a=year_icon2)] = \
                                        response.xpath(r"//tr[@class='sz'][{a}]/td[2]/text()".format(a=i + 1)).extract()[0]

                                if response.xpath(r"//tr[@class='sz'][{a}]/td[3]/text()".format(a=i + 1)).extract():
                                    school_item_like['highest_score_{a}_like'.format(a=year_icon2)] = \
                                        response.xpath(r"//tr[@class='sz'][{a}]/td[3]/text()".format(a=i + 1)).extract()[0]

                                if response.xpath(r"//tr[@class='sz'][{a}]/td[4]/text()".format(a=i + 1)).extract():
                                    school_item_like['average_score_{a}_like'.format(a=year_icon2)] = \
                                        response.xpath(r"//tr[@class='sz'][{a}]/td[4]/text()".format(a=i + 1)).extract()[0]

                                if response.xpath(r"//tr[@class='sz'][{a}]/td[5]/text()".format(a=i + 1)).extract():
                                    school_item_like['admit_people_counts_{a}_like'.format(a=year_icon2)] = \
                                        response.xpath(r"//tr[@class='sz'][{a}]/td[5]/text()".format(a=i + 1)).extract()[0]

                                if response.xpath(r"//tr[@class='sz'][{a}]/td[6]/text()".format(a=i + 1)).extract():
                                    school_item_like['admit_batch_{a}_like'.format(a=year_icon2)] = \
                                        response.xpath(r"//tr[@class='sz'][{a}]/td[6]/text()".format(a=i + 1)).extract()[0]
#aasdasdddasasddasdasdasd
                                #123113123123113131131
                #仅有一行
                else:
                    school_item_like = self.get_item()
                    year_icon2 = response.xpath(r"//tr[@class='szw'][{a}]/td[1]/text()".format(a = i + 1)).extract()[0]

                    if response.xpath(r"//div[@id='wrapper']/div[@class='cont_l in']/p[@class='btnFsxBox']/font[1]/text()").extract():
                        school_item_like['school_name'] = response.xpath(r"//div[@id='wrapper']/div[@class='cont_l in']/p[@class='btnFsxBox']/font[1]/text()").extract()[0]

                    if response.xpath(r"//div[@class='cont_l in']/p[@class='btnFsxBox']/font[2]/text()").extract():
                        school_item_like['location_name'] = response.xpath(r"//div[@class='cont_l in']/p[@class='btnFsxBox']/font[2]/text()").extract()[0]


                    if response.xpath(r"//tr[@class='szw'][{a}]/td[2]/text()".format(a=i + 1)).extract():
                        school_item_like['lowest_score_{a}_like'.format(a=year_icon2)] = \
                            response.xpath(r"//tr[@class='szw'][{a}]/td[2]/text()".format(a=i + 1)).extract()[0]

                    if response.xpath(r"//tr[@class='szw'][{a}]/td[3]/text()".format(a=i + 1)).extract():
                        school_item_like['highest_score_{a}_like'.format(a=year_icon2)] = \
                            response.xpath(r"//tr[@class='szw'][{a}]/td[3]/text()".format(a=i + 1)).extract()[0]

                    if response.xpath(r"//tr[@class='szw'][{a}]/td[4]/text()".format(a=i + 1)).extract():
                        school_item_like['average_score_{a}_like'.format(a=year_icon2)] = \
                            response.xpath(r"//tr[@class='szw'][{a}]/td[4]/text()".format(a=i + 1)).extract()[0]

                    if response.xpath(r"//tr[@class='szw'][{a}]/td[5]/text()".format(a=i + 1)).extract():
                        school_item_like['admit_people_counts_{a}_like'.format(a=year_icon2)] = \
                            response.xpath(r"//tr[@class='szw'][{a}]/td[5]/text()".format(a=i + 1)).extract()[0]

                    if response.xpath(r"//tr[@class='szw'][{a}]/td[6]/text()".format(a=i + 1)).extract():
                        school_item_like['admit_batch_{a}_like'.format(a=year_icon2)] = \
                            response.xpath(r"//tr[@class='szw'][{a}]/td[6]/text()".format(a=i + 1)).extract()[0]

                re_url_like = response.url

                re_url_wenke = '/'.join(re_url_like.split('/')[:-1]) + '/' + '2'

                yield scrapy.Request(url=re_url_wenke, callback=self.parse_item_wenke, meta={'item': school_item_like})

        #如果一行都没有
        else:
            school_item_like = re.get_item()

            
            re_url_like = response.url

            re_url_wenke = '/'.join(re_url_like.split('/')[:-1]) + '/' + '2'

            yield scrapy.Request(url=re_url_wenke, callback=self.parse_item_wenke, meta={'item': school_item_like})
            

    def parse_item_wenke(self, response):
        line_1_frame = response.xpath(r"//tr[@class='szw']/td[1]").extract()
        line_2_frame_pre = response.xpath(r"//tr[@class='sz']/td[1]").extract()

        # 如果有一行以上
        if line_1_frame:
            for i, line in enumerate(line_1_frame):

                school_item_wenke = response.meta['item']
                # 有多行
                if line_2_frame_pre:
                    # 算出偶数行的行数

                    line_2_counts = len(response.xpath(r"//tr[@class='sz']").extract())

                    # 奇数行用szw匹配
                    year_icon = response.xpath(r"//tr[@class='szw'][{a}]/td[1]/text()".format(a = i + 1)).extract()[0]

                    # 只取2010年以上的数据
                    if int(year_icon) >= 2010:

                        if response.xpath(r"//tr[@class='szw'][{a}]/td[2]/text()".format(a=i + 1)).extract():
                            school_item_wenke['lowest_score_{a}_wenke'.format(a=year_icon)] = \
                                response.xpath(r"//tr[@class='szw'][{a}]/td[2]/text()".format(a=i + 1)).extract()[0]

                        if response.xpath(r"//tr[@class='szw'][{a}]/td[3]/text()".format(a=i + 1)).extract():
                            school_item_wenke['highest_score_{a}_wenke'.format(a=year_icon)] = \
                                response.xpath(r"//tr[@class='szw'][{a}]/td[3]/text()".format(a=i + 1)).extract()[0]

                        if response.xpath(r"//tr[@class='szw'][{a}]/td[4]/text()".format(a=i + 1)).extract():
                            school_item_wenke['average_score_{a}_wenke'.format(a=year_icon)] = \
                                response.xpath(r"//tr[@class='szw'][{a}]/td[4]/text()".format(a=i + 1)).extract()[0]

                        if response.xpath(r"//tr[@class='szw'][{a}]/td[5]/text()".format(a=i + 1)).extract():
                            school_item_wenke['admit_people_counts_{a}_wenke'.format(a=year_icon)] = \
                                response.xpath(r"//tr[@class='szw'][{a}]/td[5]/text()".format(a=i + 1)).extract()[0]

                        if response.xpath(r"//tr[@class='szw'][{a}]/td[6]/text()".format(a=i + 1)).extract():
                            school_item_wenke['admit_batch_{a}_wenke'.format(a=year_icon)] = \
                                response.xpath(r"//tr[@class='szw'][{a}]/td[6]/text()".format(a=i + 1)).extract()[0]
                        
                        
                    # the1_line_year = response.xpath(r"//tr[@class='szw'][1]/td[1]/text()").extract()[0]
                    # the2_line_year = response.xpath(r"//tr[@class='szw'][1]/td[1]/text()").extract()[0]
                    # the1_line_year = response.xpath(r"//tr[@class='szw'][1]/td[1]/text()").extract()

                    # 偶数行用sz匹配
                    if i <= line_2_counts:

                        if response.xpath(r"//tr[@class='sz'][{a}]/td[1]/text()".format(a = i + 1)).extract():
                            year_icon = response.xpath(r"//tr[@class='sz'][{a}]/td[1]/text()".format(a = i + 1)).extract()[0]

                            # 只取2010年以上的数据
                            if int(year_icon) >= 2010:

                                if response.xpath(r"//tr[@class='sz'][{a}]/td[2]/text()".format(a=i + 1)).extract():
                                    school_item_wenke['lowest_score_{a}_wenke'.format(a=year_icon)] = \
                                        response.xpath(r"//tr[@class='sz'][{a}]/td[2]/text()".format(a=i + 1)).extract()[0]

                                if response.xpath(r"//tr[@class='sz'][{a}]/td[3]/text()".format(a=i + 1)).extract():
                                    school_item_wenke['highest_score_{a}_wenke'.format(a=year_icon)] = \
                                        response.xpath(r"//tr[@class='sz'][{a}]/td[3]/text()".format(a=i + 1)).extract()[0]

                                if response.xpath(r"//tr[@class='sz'][{a}]/td[4]/text()".format(a=i + 1)).extract():
                                    school_item_wenke['average_score_{a}_wenke'.format(a=year_icon)] = \
                                        response.xpath(r"//tr[@class='sz'][{a}]/td[4]/text()".format(a=i + 1)).extract()[0]

                                if response.xpath(r"//tr[@class='sz'][{a}]/td[5]/text()".format(a=i + 1)).extract():
                                    school_item_wenke['admit_people_counts_{a}_wenke'.format(a=year_icon)] = \
                                        response.xpath(r"//tr[@class='sz'][{a}]/td[5]/text()".format(a=i + 1)).extract()[0]

                                if response.xpath(r"//tr[@class='sz'][{a}]/td[6]/text()".format(a=i + 1)).extract():
                                    school_item_wenke['admit_batch_{a}_wenke'.format(a=year_icon)] = \
                                        response.xpath(r"//tr[@class='sz'][{a}]/td[6]/text()".format(a=i + 1)).extract()[0]

                # 仅有一行
                else:
                    school_item_wenke = response.meta['item']

                    if response.xpath(r"//tr[@class='szw'][{a}]/td[1]/text()".format(a=i)).extract():

                        year_icon = response.xpath(r"//tr[@class='szw'][{a}]/td[1]/text()".format(a=i)).extract()[0]

                        school_item_wenke['lowest_score_{a}_wenke'.format(a=year_icon)] = \
                            response.xpath(r"//tr[@class='szw'][1]/td[2]/text()").extract()[0]

                        school_item_wenke['highest_score_{a}_wenke'.format(a=year_icon)] = \
                            response.xpath(r"//tr[@class='szw'][1]/td[3]/text()").extract()[0]

                        school_item_wenke['average_score_{a}_wenke'.format(a=year_icon)] = \
                            response.xpath(r"//tr[@class='szw'][1]/td[4]/text()").extract()[0]

                        school_item_wenke['admit_people_counts_{a}_wenke'.format(a=year_icon)] = \
                            response.xpath(r"//tr[@class='szw'][1]/td[5]/text()").extract()[0]

                        school_item_wenke['admit_batch_{a}_wenke'.format(a=year_icon)] = \
                            response.xpath(r"//tr[@class='szw'][1]/td[6]/text()").extract()[0]

                yield school_item_wenke


        else:
            school_item_wenke = response.meta['item']

            yield school_item_wenke


    def get_item(self):
        school_item_like = GaokaowangItem_school_scoreline()

        school_item_like['school_name'] = '------'
        school_item_like['location_name'] = '------'
        school_item_like['lowest_score_2017_like_l1'] = '------'
        school_item_like['highest_score_2017_like_l1'] = '------'
        school_item_like['average_score_2017_like_l1'] = '------'
        school_item_like['admit_people_counts_2017_like_l1'] = '------'
        school_item_like['admit_batch_2017_like_l1'] = '------'
        school_item_like['lowest_score_2016_like_l1'] = '------'
        school_item_like['highest_score_2016_like_l1'] = '------'
        school_item_like['average_score_2016_like_l1'] = '------'
        school_item_like['admit_people_counts_2016_like_l1'] = '------'
        school_item_like['admit_batch_2016_like_l1'] = '------'
        school_item_like['lowest_score_2015_like_l1'] = '------'
        school_item_like['highest_score_2015_like_l1'] = '------'
        school_item_like['average_score_2015_like_l1'] = '------'
        school_item_like['admit_people_counts_2015_like_l1'] = '------'
        school_item_like['admit_batch_2015_like_l1'] = '------'
        school_item_like['lowest_score_2014_like_l1'] = '------'
        school_item_like['highest_score_2014_like_l1'] = '------'
        school_item_like['average_score_2014_like_l1'] = '------'
        school_item_like['admit_people_counts_2014_like_l1'] = '------'
        school_item_like['admit_batch_2014_like_l1'] = '------'
        school_item_like['lowest_score_2013_like_l1'] = '------'
        school_item_like['highest_score_2013_like_l1'] = '------'
        school_item_like['average_score_2013_like_l1'] = '------'
        school_item_like['admit_people_counts_2013_like_l1'] = '------'
        school_item_like['admit_batch_2013_like_l1'] = '------'
        school_item_like['lowest_score_2012_like_l1'] = '------'
        school_item_like['highest_score_2012_like_l1'] = '------'
        school_item_like['average_score_2012_like_l1'] = '------'
        school_item_like['admit_people_counts_2012_like_l1'] = '------'
        school_item_like['admit_batch_2012_like_l1'] = '------'
        school_item_like['lowest_score_2011_like_l1'] = '------'
        school_item_like['highest_score_2011_like_l1'] = '------'
        school_item_like['average_score_2011_like_l1'] = '------'
        school_item_like['admit_people_counts_2011_like_l1'] = '------'
        school_item_like['admit_batch_2011_like_l1'] = '------'
        school_item_like['lowest_score_2010_like_l1'] = '------'
        school_item_like['highest_score_2010_like_l1'] = '------'
        school_item_like['average_score_2010_like_l1'] = '------'
        school_item_like['admit_people_counts_2010_like_l1'] = '------'
        school_item_like['admit_batch_2010_like_l1'] = '------'
        
        school_item_like['lowest_score_2017_like_l2'] = '------'
        school_item_like['highest_score_2017_like_l2'] = '------'
        school_item_like['average_score_2017_like_l2'] = '------'
        school_item_like['admit_people_counts_2017_like_l2'] = '------'
        school_item_like['admit_batch_2017_like_l2'] = '------'
        school_item_like['lowest_score_2016_like_l2'] = '------'
        school_item_like['highest_score_2016_like_l2'] = '------'
        school_item_like['average_score_2016_like_l2'] = '------'
        school_item_like['admit_people_counts_2016_like_l2'] = '------'
        school_item_like['admit_batch_2016_like_l2'] = '------'
        school_item_like['lowest_score_2015_like_l2'] = '------'
        school_item_like['highest_score_2015_like_l2'] = '------'
        school_item_like['average_score_2015_like_l2'] = '------'
        school_item_like['admit_people_counts_2015_like_l2'] = '------'
        school_item_like['admit_batch_2015_like_l2'] = '------'
        school_item_like['lowest_score_2014_like_l2'] = '------'
        school_item_like['highest_score_2014_like_l2'] = '------'
        school_item_like['average_score_2014_like_l2'] = '------'
        school_item_like['admit_people_counts_2014_like_l2'] = '------'
        school_item_like['admit_batch_2014_like_l2'] = '------'
        school_item_like['lowest_score_2013_like_l2'] = '------'
        school_item_like['highest_score_2013_like_l2'] = '------'
        school_item_like['average_score_2013_like_l2'] = '------'
        school_item_like['admit_people_counts_2013_like_l2'] = '------'
        school_item_like['admit_batch_2013_like_l2'] = '------'
        school_item_like['lowest_score_2012_like_l2'] = '------'
        school_item_like['highest_score_2012_like_l2'] = '------'
        school_item_like['average_score_2012_like_l2'] = '------'
        school_item_like['admit_people_counts_2012_like_l2'] = '------'
        school_item_like['admit_batch_2012_like_l2'] = '------'
        school_item_like['lowest_score_2011_like_l2'] = '------'
        school_item_like['highest_score_2011_like_l2'] = '------'
        school_item_like['average_score_2011_like_l2'] = '------'
        school_item_like['admit_people_counts_2011_like_l2'] = '------'
        school_item_like['admit_batch_2011_like_l2'] = '------'
        school_item_like['lowest_score_2010_like_l2'] = '------'
        school_item_like['highest_score_2010_like_l2'] = '------'
        school_item_like['average_score_2010_like_l2'] = '------'
        school_item_like['admit_people_counts_2010_like_l2'] = '------'
        school_item_like['admit_batch_2010_like_l2'] = '------'
        
        school_item_like['lowest_score_2017_like_l3'] = '------'
        school_item_like['highest_score_2017_like_l3'] = '------'
        school_item_like['average_score_2017_like_l3'] = '------'
        school_item_like['admit_people_counts_2017_like_l3'] = '------'
        school_item_like['admit_batch_2017_like_l3'] = '------'
        school_item_like['lowest_score_2016_like_l3'] = '------'
        school_item_like['highest_score_2016_like_l3'] = '------'
        school_item_like['average_score_2016_like_l3'] = '------'
        school_item_like['admit_people_counts_2016_like_l3'] = '------'
        school_item_like['admit_batch_2016_like_l3'] = '------'
        school_item_like['lowest_score_2015_like_l3'] = '------'
        school_item_like['highest_score_2015_like_l3'] = '------'
        school_item_like['average_score_2015_like_l3'] = '------'
        school_item_like['admit_people_counts_2015_like_l3'] = '------'
        school_item_like['admit_batch_2015_like_l3'] = '------'
        school_item_like['lowest_score_2014_like_l3'] = '------'
        school_item_like['highest_score_2014_like_l3'] = '------'
        school_item_like['average_score_2014_like_l3'] = '------'
        school_item_like['admit_people_counts_2014_like_l3'] = '------'
        school_item_like['admit_batch_2014_like_l3'] = '------'
        school_item_like['lowest_score_2013_like_l3'] = '------'
        school_item_like['highest_score_2013_like_l3'] = '------'
        school_item_like['average_score_2013_like_l3'] = '------'
        school_item_like['admit_people_counts_2013_like_l3'] = '------'
        school_item_like['admit_batch_2013_like_l3'] = '------'
        school_item_like['lowest_score_2012_like_l3'] = '------'
        school_item_like['highest_score_2012_like_l3'] = '------'
        school_item_like['average_score_2012_like_l3'] = '------'
        school_item_like['admit_people_counts_2012_like_l3'] = '------'
        school_item_like['admit_batch_2012_like_l3'] = '------'
        school_item_like['lowest_score_2011_like_l3'] = '------'
        school_item_like['highest_score_2011_like_l3'] = '------'
        school_item_like['average_score_2011_like_l3'] = '------'
        school_item_like['admit_people_counts_2011_like_l3'] = '------'
        school_item_like['admit_batch_2011_like_l3'] = '------'
        school_item_like['lowest_score_2010_like_l3'] = '------'
        school_item_like['highest_score_2010_like_l3'] = '------'
        school_item_like['average_score_2010_like_l3'] = '------'
        school_item_like['admit_people_counts_2010_like_l3'] = '------'
        school_item_like['admit_batch_2010_like_l3'] = '------'

        school_item_like = GaokaowangItem_school_scoreline()
        school_item_like['school_name'] = '------'
        school_item_like['location_name'] = '------'
        school_item_like['lowest_score_2017_wenke_l1'] = '------'
        school_item_like['highest_score_2017_wenke_l1'] = '------'
        school_item_like['average_score_2017_wenke_l1'] = '------'
        school_item_like['admit_people_counts_2017_wenke_l1'] = '------'
        school_item_like['admit_batch_2017_wenke_l1'] = '------'
        school_item_like['lowest_score_2016_wenke_l1'] = '------'
        school_item_like['highest_score_2016_wenke_l1'] = '------'
        school_item_like['average_score_2016_wenke_l1'] = '------'
        school_item_like['admit_people_counts_2016_wenke_l1'] = '------'
        school_item_like['admit_batch_2016_wenke_l1'] = '------'
        school_item_like['lowest_score_2015_wenke_l1'] = '------'
        school_item_like['highest_score_2015_wenke_l1'] = '------'
        school_item_like['average_score_2015_wenke_l1'] = '------'
        school_item_like['admit_people_counts_2015_wenke_l1'] = '------'
        school_item_like['admit_batch_2015_wenke_l1'] = '------'
        school_item_like['lowest_score_2014_wenke_l1'] = '------'
        school_item_like['highest_score_2014_wenke_l1'] = '------'
        school_item_like['average_score_2014_wenke_l1'] = '------'
        school_item_like['admit_people_counts_2014_wenke_l1'] = '------'
        school_item_like['admit_batch_2014_wenke_l1'] = '------'
        school_item_like['lowest_score_2013_wenke_l1'] = '------'
        school_item_like['highest_score_2013_wenke_l1'] = '------'
        school_item_like['average_score_2013_wenke_l1'] = '------'
        school_item_like['admit_people_counts_2013_wenke_l1'] = '------'
        school_item_like['admit_batch_2013_wenke_l1'] = '------'
        school_item_like['lowest_score_2012_wenke_l1'] = '------'
        school_item_like['highest_score_2012_wenke_l1'] = '------'
        school_item_like['average_score_2012_wenke_l1'] = '------'
        school_item_like['admit_people_counts_2012_wenke_l1'] = '------'
        school_item_like['admit_batch_2012_wenke_l1'] = '------'
        school_item_like['lowest_score_2011_wenke_l1'] = '------'
        school_item_like['highest_score_2011_wenke_l1'] = '------'
        school_item_like['average_score_2011_wenke_l1'] = '------'
        school_item_like['admit_people_counts_2011_wenke_l1'] = '------'
        school_item_like['admit_batch_2011_wenke_l1'] = '------'
        school_item_like['lowest_score_2010_wenke_l1'] = '------'
        school_item_like['highest_score_2010_wenke_l1'] = '------'
        school_item_like['average_score_2010_wenke_l1'] = '------'
        school_item_like['admit_people_counts_2010_wenke_l1'] = '------'
        school_item_like['admit_batch_2010_wenke_l1'] = '------'
        
        school_item_like['lowest_score_2017_wenke_l2'] = '------'
        school_item_like['highest_score_2017_wenke_l2'] = '------'
        school_item_like['average_score_2017_wenke_l2'] = '------'
        school_item_like['admit_people_counts_2017_wenke_l2'] = '------'
        school_item_like['admit_batch_2017_wenke_l2'] = '------'
        school_item_like['lowest_score_2016_wenke_l2'] = '------'
        school_item_like['highest_score_2016_wenke_l2'] = '------'
        school_item_like['average_score_2016_wenke_l2'] = '------'
        school_item_like['admit_people_counts_2016_wenke_l2'] = '------'
        school_item_like['admit_batch_2016_wenke_l2'] = '------'
        school_item_like['lowest_score_2015_wenke_l2'] = '------'
        school_item_like['highest_score_2015_wenke_l2'] = '------'
        school_item_like['average_score_2015_wenke_l2'] = '------'
        school_item_like['admit_people_counts_2015_wenke_l2'] = '------'
        school_item_like['admit_batch_2015_wenke_l2'] = '------'
        school_item_like['lowest_score_2014_wenke_l2'] = '------'
        school_item_like['highest_score_2014_wenke_l2'] = '------'
        school_item_like['average_score_2014_wenke_l2'] = '------'
        school_item_like['admit_people_counts_2014_wenke_l2'] = '------'
        school_item_like['admit_batch_2014_wenke_l2'] = '------'
        school_item_like['lowest_score_2013_wenke_l2'] = '------'
        school_item_like['highest_score_2013_wenke_l2'] = '------'
        school_item_like['average_score_2013_wenke_l2'] = '------'
        school_item_like['admit_people_counts_2013_wenke_l2'] = '------'
        school_item_like['admit_batch_2013_wenke_l2'] = '------'
        school_item_like['lowest_score_2012_wenke_l2'] = '------'
        school_item_like['highest_score_2012_wenke_l2'] = '------'
        school_item_like['average_score_2012_wenke_l2'] = '------'
        school_item_like['admit_people_counts_2012_wenke_l2'] = '------'
        school_item_like['admit_batch_2012_wenke_l2'] = '------'
        school_item_like['lowest_score_2011_wenke_l2'] = '------'
        school_item_like['highest_score_2011_wenke_l2'] = '------'
        school_item_like['average_score_2011_wenke_l2'] = '------'
        school_item_like['admit_people_counts_2011_wenke_l2'] = '------'
        school_item_like['admit_batch_2011_wenke_l2'] = '------'
        school_item_like['lowest_score_2010_wenke_l2'] = '------'
        school_item_like['highest_score_2010_wenke_l2'] = '------'
        school_item_like['average_score_2010_wenke_l2'] = '------'
        school_item_like['admit_people_counts_2010_wenke_l2'] = '------'
        school_item_like['admit_batch_2010_wenke_l2'] = '------'
        
        school_item_like['lowest_score_2017_wenke_l3'] = '------'
        school_item_like['highest_score_2017_wenke_l3'] = '------'
        school_item_like['average_score_2017_wenke_l3'] = '------'
        school_item_like['admit_people_counts_2017_wenke_l3'] = '------'
        school_item_like['admit_batch_2017_wenke_l3'] = '------'
        school_item_like['lowest_score_2016_wenke_l3'] = '------'
        school_item_like['highest_score_2016_wenke_l3'] = '------'
        school_item_like['average_score_2016_wenke_l3'] = '------'
        school_item_like['admit_people_counts_2016_wenke_l3'] = '------'
        school_item_like['admit_batch_2016_wenke_l3'] = '------'
        school_item_like['lowest_score_2015_wenke_l3'] = '------'
        school_item_like['highest_score_2015_wenke_l3'] = '------'
        school_item_like['average_score_2015_wenke_l3'] = '------'
        school_item_like['admit_people_counts_2015_wenke_l3'] = '------'
        school_item_like['admit_batch_2015_wenke_l3'] = '------'
        school_item_like['lowest_score_2014_wenke_l3'] = '------'
        school_item_like['highest_score_2014_wenke_l3'] = '------'
        school_item_like['average_score_2014_wenke_l3'] = '------'
        school_item_like['admit_people_counts_2014_wenke_l3'] = '------'
        school_item_like['admit_batch_2014_wenke_l3'] = '------'
        school_item_like['lowest_score_2013_wenke_l3'] = '------'
        school_item_like['highest_score_2013_wenke_l3'] = '------'
        school_item_like['average_score_2013_wenke_l3'] = '------'
        school_item_like['admit_people_counts_2013_wenke_l3'] = '------'
        school_item_like['admit_batch_2013_wenke_l3'] = '------'
        school_item_like['lowest_score_2012_wenke_l3'] = '------'
        school_item_like['highest_score_2012_wenke_l3'] = '------'
        school_item_like['average_score_2012_wenke_l3'] = '------'
        school_item_like['admit_people_counts_2012_wenke_l3'] = '------'
        school_item_like['admit_batch_2012_wenke_l3'] = '------'
        school_item_like['lowest_score_2011_wenke_l3'] = '------'
        school_item_like['highest_score_2011_wenke_l3'] = '------'
        school_item_like['average_score_2011_wenke_l3'] = '------'
        school_item_like['admit_people_counts_2011_wenke_l3'] = '------'
        school_item_like['admit_batch_2011_wenke_l3'] = '------'
        school_item_like['lowest_score_2010_wenke_l3'] = '------'
        school_item_like['highest_score_2010_wenke_l3'] = '------'
        school_item_like['average_score_2010_wenke_l3'] = '------'
        school_item_like['admit_people_counts_2010_wenke_l3'] = '------'
        school_item_like['admit_batch_2010_wenke_l3'] = '------'
        
        
        return school_item_like

