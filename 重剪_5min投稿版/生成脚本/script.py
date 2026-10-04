# Eye2Eye 投稿视频（≤5 min）分镜数据。
# 每个 shot: id, sec(章节), vis(画面: ("slide", name) 或 ("footage", 素材名, 画面说明, 缩略图或None)),
# lines: [(speaker, 字幕文本, 可选TTS文本)]，speaker ∈ N(旁白) / AI / U(用户)
# label: 画面角标（功能点提示），min: 最短时长(秒)

S = []
def shot(id, sec, vis, lines=(), label="", min=0.0, note=""):
    S.append(dict(id=id, sec=sec, vis=vis, lines=list(lines), label=label, min=min, note=note))

E = "Eye-to-Eye"  # TTS 读法

# ---------- 0 开场 ----------
shot("0.1", "Opening", ("footage", "t开头2.MP4", "全家书架远景，杂乱的书堆", "shelf"),
     [("N", "When people work side by side, a glance or a gesture is often enough to be understood.")])
shot("0.2", "Opening", ("footage", "t戴眼镜.MP4", "第三人称：用户戴上 Vision Pro 站在书架前", "avp"),
     [("N", "Can an AI assistant that sees through our eyes collaborate the same way?")])
shot("0.3", "Opening", ("slide", "title"), [], min=4.5)

# ---------- 1 研究动机 ----------
shot("1.1", "Motivation", ("footage", "t开头放回.MP4", "用户拿起书又放回，犹豫不决", "shelf2"),
     [("N", "Imagine organizing a crowded family bookshelf, with Dad's classics, your sister's picture books, and your own textbooks, helped by an AI assistant in your glasses.")])
shot("1.2", "Motivation", ("slide", "gulf_comm"),
     [("N", "Today's assistants make you translate what you see and do into words. Rich, parallel physical intent gets squeezed into a single verbal channel. This is the communication gulf.")])
shot("1.3", "Motivation", ("slide", "gulf_under"),
     [("N", "And even when the AI recognizes objects, it misses embodied cues, like a hesitant gaze or a pause with a book in hand, and it forgets the personal rules you just agreed on. This is the understanding gulf.")])
shot("1.4", "Motivation", ("slide", "rq"),
     [("N", "So we ask: how can a shared first-person perspective enable continuous cognitive alignment between humans and AI?")])

# ---------- 2 框架 ----------
shot("2.1", "Framework", ("slide", "fig2"),
     [("N", "We introduce Eye2Eye, a framework that turns the first-person view from a passive input into a shared channel for collaboration. It closes a loop of three components.",
       f"We introduce {E}, a framework that turns the first-person view from a passive input into a shared channel for collaboration. It closes a loop of three components.")])
shot("2.2", "Framework", ("slide", "fig3_human"),
     [("N", "One: joint attention. From human to AI, Eye2Eye captures speech, gaze, and gestures such as pointing, touching, and grasping, to detect interaction events and infer intent.",
       f"One: joint attention. From human to AI, {E} captures speech, gaze, and gestures such as pointing, touching, and grasping, to detect interaction events and infer intent.")],
     label="I · Joint Attention")
shot("2.3", "Framework", ("footage", "VID_0007.AVI", "Vision Pro 第一人称录屏：AI 对目标物体的高亮框 + 文字标签", "pip_ux"),
     [("N", "From AI to human, it makes its own focus visible through visual highlights, voice, and text labels, so both partners converge on the same object.")],
     label="I · AI → Human")
shot("2.4", "Framework", ("slide", "fig5"),
     [("N", "Two: accumulated common ground. Each interaction is stored in a dynamic object card: what the object is, what the user intended, how the AI responded, and whether it worked. Cards persist, and they are revised whenever the AI is corrected.")],
     label="II · Common Ground")
shot("2.5", "Framework", ("slide", "fig6"),
     [("N", "Three: reflective situated feedback. Using that common ground, the AI picks one of four strategies: object recognition, error checking, knowledge recall, or action planning, each mixing visual and verbal cues. It then watches how the user reacts, and writes the outcome back to memory.")],
     label="III · Situated Feedback")
shot("2.6", "Framework", ("slide", "fig2"),
     [("N", "Together, these components form a continuous perceive, align, and reflect loop.")])

# ---------- 3 系统与技术方案 ----------
shot("3.1", "System", ("slide", "fig4_I"),
     [("N", "Our prototype runs on Apple Vision Pro. YOLO tracks objects in the first-person view. When a hand overlaps an object, or gaze dwells on it for six seconds, an event fires, and GPT-4o interprets the frame together with the user's speech.")],
     label="Joint Attention pipeline")
shot("3.2", "System", ("slide", "fig4_II"),
     [("N", "That state is embedded and matched against existing object cards by cosine similarity. The best match is retrieved, fused with the current state, and the card is created or updated.")],
     label="Object-card memory (RAG)")
shot("3.3", "System", ("slide", "fig4_III"),
     [("N", "Finally, the model selects a feedback strategy and modality, rendered in AR and spoken with Gemini text-to-speech, in about four to five seconds end to end.")],
     label="Feedback generation")

# ---------- 4 Demo ----------
shot("4.1", "Demo", ("footage", "t开头2.MP4 / t戴眼镜.MP4", "用户戴好头显走向书架（可接一个第一人称转场）", "avp"),
     [("N", "Let's walk through a complete example.")])
shot("4.2", "Demo", ("footage", "great.MOV + Business Book.png", "第一人称：拿起《Great by Choice》，AI 高亮书本并弹出文字标签 “Business Book”", None),
     [("U", "What kind of book is this?"),
      ("AI", "\"Great by Choice\" is a business book.")],
     label="Object Recognition · text label + short voice")
shot("4.3", "Demo", ("footage", "t右上.MP4 / t右上2.MP4", "用户拿着书在两层书架间来回看，手悬停；画面角落显示 AI 推理文字", None),
     [("N", "When the user hesitates, Eye2Eye picks up the cue from gaze and hand movement, without being asked.",
       f"When the user hesitates, {E} picks up the cue from gaze and hand movement, without being asked."),
      ("AI", "I recommend the Toolkit category for easy access, rather than the Design category.")],
     label="Implicit cue · hesitation")
shot("4.4", "Demo", ("footage", "1鱼.MP4 / t鱼.MP4", "第一人称：双手拿起《OCEAN》立体书，注视点停留（见缩略图）", "ocean"),
     [("U", "I should put this book in..."),
      ("AI", "You can put this book in the Biology section."),
      ("U", "I don't think Biology is the right fit. My little sister loves these books specifically, not the whole Biology category.")],
     label="Action Planning")
shot("4.5", "Demo", ("footage", "t灵机一动.MP4 + 灯泡贴纸", "用户恍然、AI 新建分区；书架上出现 “Children's Reading” 标签", "ocean2"),
     [("AI", "Okay, let's create a new section for this, called Children's Reading."),
      ("N", "The correction is written back into the object card.")],
     label="Common ground revised")
shot("4.6", "Demo", ("footage", "t恐龙.MP4", "拿起恐龙书，AI 直接高亮 Children's Reading 分区", None),
     [("U", "Where should I put this one?"),
      ("AI", "The dinosaur book should go in Children's Reading as well.")],
     label="Memory reused")
shot("4.7", "Demo", ("footage", "画.MOV / 画2.MOV + Visual Arts Category.png", "两本主题不同的画册并排，AI 归入 Visual Arts", None),
     [("U", "These books aren't on the same theme. Do they go in the same category?"),
      ("AI", "Based on our earlier agreement, these books are mainly images and photographs, so they belong in Visual Arts.")],
     label="Knowledge Recall · text label + detailed voice")
shot("4.8", "Demo", ("footage", "金字塔.MOV", "用户把《金字塔原理》放入表达训练区，AI 红框提示并指向思维训练区", None),
     [("U", "Let's put this in Expression Training."),
      ("AI", "That category isn't quite right. Thinking Training keeps it with the rest of the Pyramid Principle series.")],
     label="Error Checking · visual overlay + detailed voice")
shot("4.9", "Demo", ("slide", "fig7"),
     [("N", "Beyond bookshelves, the same loop guides procedural tasks like operating a coffee machine, and inspection tasks like troubleshooting a circuit board.")],
     label="Also: coffee machine · circuit board")

# ---------- 5 实验结果 ----------
shot("5.1", "Results", ("slide", "study"),
     [("N", "We compared Eye2Eye with a baseline using the same headset and models, in a study with sixty participants and three tasks.",
       f"We compared {E} with a baseline using the same headset and models, in a study with sixty participants and three tasks.")])
shot("5.2", "Results", ("slide", "numbers"),
     [("N", "Eye2Eye reduced the likelihood of errors by about fifty-eight percent, cut clarification turns by half, and reduced interaction turns in the procedural task by twenty-three percent.",
       f"{E} reduced the likelihood of errors by about fifty-eight percent, cut clarification turns by half, and reduced interaction turns in the procedural task by twenty-three percent.")])
shot("5.3", "Results", ("slide", "fig89"),
     [("N", "Errors also accumulated far more slowly over time, and participants rated the collaboration as significantly more fluent, more co-present, and more trustworthy.")])

# ---------- 6 结尾 ----------
shot("6.1", "Closing", ("footage", "t开头2.MP4（整理完成的书架）", "整理完成的书架远景，缓慢推近", "shelf"),
     [("N", "By sharing what we see, humans and AI can do more than look at the same thing. They can truly see eye to eye.")])
shot("6.2", "Closing", ("slide", "end"), [], min=5.5)
