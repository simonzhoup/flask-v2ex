from V2DE import db,Tag,Node


def fill_tag():
    tags = ['技术','创意','好玩','Apple','酷工作','交易','城市','问与答','最热','全部','节点关注']
    for t in tags:
        tag = Tag(name=t)
        db.session.add(tag)
        db.session.commit()
    return 'Done'

def populate_node():
    data = {
        '技术':['程序员','Python','iDev','Android','Linux','node.js','云计算','宽带症候群'],
        '创意':['分享创造','设计','奇思妙想'],
        '好玩':['分享发现','电子游戏','电影','剧集','音乐','旅游','午夜俱乐部'],
        'Apple':['macOS','iPhone','iPad','MBP','iMac','WATCH','Apple'],
        '酷工作':['酷工作','求职','职场话题','外包'],
        '交易':['二手交易','物物交换','免费赠送','域名','团购','安全提示'],
        '城市':['北京','上海','深圳','广州','杭州','成都','昆明','纽约','杉矶'],
        '问与答':['问与答'],
        '全部':['分享发现','分享创造','问与答','酷工作','程序员','职场话题','奇思妙想','优惠信息']
    }
    for t in data.keys():
        tag = Tag.query.filter_by(name=t).first()
        if tag:
            for n in data[t]:
                if not Node.query.filter_by(name=n).first():
                    node = Node(name=n,tag_id=tag.id)
                    db.session.add(node)
                    db.session.commit()
    return 'Done'