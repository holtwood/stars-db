"""StarsDB 分类配置:GitHub Star Lists → 分类页映射

维护方法:
- GitHub Star Lists(28 个)通过 lists_meta.json 拉取
- 一个分类页可由多个 list 聚合而成(如 'ai' = AI与LLM + AI-Agent与MCP + AI-Infra)
- 新增分类页:在此添加一项,并在 docs/ 下由 gen_index.py 自动生成
"""
import datetime

# ---------- 分类配置(对齐 28 个 list,按领域分组) ----------
CATEGORIES = [
    {
        'key': 'ai', 'title': 'AI 与 LLM', 'emoji': '🤖',
        'desc': '大模型、训练/推理框架、Agent、MCP 生态',
        'lists': ['AI与LLM', 'AI-Agent与MCP', 'AI-Infra'],
    },
    {
        'key': 'devops', 'title': 'DevOps 与云原生', 'emoji': '☁️',
        'desc': '容器、编排、CI/CD、自托管',
        'lists': ['DevOps与云原生'],
    },
    {
        'key': 'lang', 'title': '语言生态', 'emoji': '🧩',
        'desc': 'Python / Go / Rust / C++ / JVM 等语言库与工具',
        'lists': ['Python生态', 'Go生态', 'Rust生态', 'Modern-C++', 'JVM与其他语言'],
    },
    {
        'key': 'frontend', 'title': '前端与 Web', 'emoji': '🎨',
        'desc': '前端框架、Web 应用与资源',
        'lists': ['前端与Web'],
    },
    {
        'key': 'cli', 'title': 'CLI 与终端', 'emoji': '⌨️',
        'desc': '命令行工具、终端效率、系统与桌面工具',
        'lists': ['CLI与终端工具', '系统与桌面工具', '主题与字体'],
    },
    {
        'key': 'storage', 'title': '数据库与存储', 'emoji': '🗄️',
        'desc': '数据库、缓存与存储系统',
        'lists': ['数据库与存储'],
    },
    {
        'key': 'security', 'title': '安全与逆向', 'emoji': '🔐',
        'desc': '安全工具、逆向工程、隐私',
        'lists': ['安全与逆向'],
    },
    {
        'key': 'net', 'title': '网络与代理', 'emoji': '🌐',
        'desc': '代理客户端、规则集与网络工具',
        'lists': ['网络与代理'],
    },
    {
        'key': 'multimedia', 'title': '图形与音视频', 'emoji': '🎬',
        'desc': '图形、图像、音频、视频处理',
        'lists': ['图形与音视频'],
    },
    {
        'key': 'browser', 'title': '浏览器扩展', 'emoji': '🧩',
        'desc': '浏览器扩展与用户脚本',
        'lists': ['浏览器扩展'],
    },
    {
        'key': 'mobile', 'title': '移动开发', 'emoji': '📱',
        'desc': 'Android / iOS / 跨平台移动开发',
        'lists': ['移动开发'],
    },
    {
        'key': 'notes', 'title': '编辑器与文档笔记', 'emoji': '📝',
        'desc': '编辑器、Markdown、笔记与知识管理',
        'lists': ['编辑器与文档笔记'],
    },
    {
        'key': 'algo', 'title': '算法与面试', 'emoji': '🧮',
        'desc': '算法题、面试准备、竞赛编程',
        'lists': ['算法与面试'],
    },
    {
        'key': 'hpc', 'title': '高性能计算', 'emoji': '⚡',
        'desc': 'HPC、CUDA/GPU 计算、性能优化',
        'lists': ['高性能计算'],
    },
    {
        'key': 'compression', 'title': '压缩与编码', 'emoji': '🗜️',
        'desc': '压缩算法与编码库',
        'lists': ['压缩与编码'],
    },
    {
        'key': 'bio', 'title': '生物信息', 'emoji': '🧬',
        'desc': '生物信息学算法与工具',
        'lists': ['BioInfoAlgo'],
    },
    {
        'key': 'learning', 'title': '学习资源与清单', 'emoji': '📚',
        'desc': '教程、书籍、awesome 清单、学习路线',
        'lists': ['学习资源与清单'],
    },
    {
        'key': 'interview', 'title': '面试资料', 'emoji': '🎯',
        'desc': '面试资料专项',
        'lists': ['面试资料'],
    },
    {
        'key': 'misc', 'title': '其他与杂项', 'emoji': '📦',
        'desc': '未归类、杂项与有效工具',
        'lists': ['其他与杂项', '有效工具'],
    },
]

# 全量索引文件名(自动生成)
ALL_INDEX = 'all.md'
LANG_INDEX = 'by-language.md'

# 仓库基础信息
REPO = 'stars-db'
OWNER = 'LessUp'
STAR_LISTS_URL = 'https://github.com/LessUp?tab=stars'

def today() -> str:
    return datetime.date.today().isoformat()
