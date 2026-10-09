<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #1A5F7A', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#1A5F7A' }}>M0 痛点破冰 ＋ M1 工具熟悉</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>用一线原声共鸣，用两步/三步上手 —— 课标锚点：八上U3 / 七上U1</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'row', gap:18, marginTop:14, alignItems:'stretch' }}>
    <Box style={{ flex:1, background:'#FCEBEA', borderRadius:12, padding:'18px 20px' }}>
      <Text style={{ fontSize:22, fontWeight:'bold', color:'#C0392B' }}>M0 · 6 大真实痛点</Text>
      {['讲评课学生被动走神','词汇听默单调、学生讨厌','早读不敢开口、一片沉默','写作结构记不住，背模板也写不出','语法备课翻倍，资料翻一周','听力检测难兼顾趣味与实效'].map((p, i) => (
        <Box key={i} style={{ flexDirection:'row', gap:10, alignItems:'flex-start', marginTop:12 }}>
          <Text style={{ fontSize:20, fontWeight:'bold', color:'#C0392B', fontFamily:'Arial' }}>{i+1}</Text>
          <Text style={{ fontSize:17, color:'#1F2937', lineHeight:1.5, flex:1 }}>{p}</Text>
        </Box>
      ))}
      <Text style={{ fontSize:15, color:'#9A3412', marginTop:12, fontStyle:'italic' }}>产出：写下"我最想 AI 帮我解决的 1 个痛点"贴墙</Text>
    </Box>
    <Box style={{ flex:1.1, background:'#F4F8FA', borderRadius:12, padding:'18px 20px' }}>
      <Text style={{ fontSize:22, fontWeight:'bold', color:'#1A5F7A' }}>M1 · 工具上手（零门槛）</Text>
      <Box style={{ marginTop:12, background:'#FFFFFF', borderRadius:8, padding:'12px 14px' }}>
        <Text style={{ fontSize:17, fontWeight:'bold', color:'#1A5F7A' }}>飞象老师 · 两步</Text>
        <Text style={{ fontSize:16, color:'#1F2937', lineHeight:1.6, marginTop:4 }}>① 国家平台账号登录　② 选"用AI"→飞象老师→模板→生成互动页</Text>
      </Box>
      <Box style={{ marginTop:12, background:'#FFFFFF', borderRadius:8, padding:'12px 14px' }}>
        <Text style={{ fontSize:17, fontWeight:'bold', color:'#C2410C' }}>豆包 / DeepSeek · 三步</Text>
        <Text style={{ fontSize:16, color:'#1F2937', lineHeight:1.6, marginTop:4 }}>① 打开网页　② 粘提示词　③ 复制结果</Text>
      </Box>
      <Box style={{ marginTop:12, background:'#FFF7ED', borderRadius:8, padding:'12px 14px', borderLeft:'4px solid #F57C00' }}>
        <Text style={{ fontSize:15, color:'#1F2937', lineHeight:1.5 }}>演练（七上U1 This is me!）：<br />"你是 10 年教龄英语教师，为七年级设计 My Self-introduction 写作清单，含 5 项 + 范例 + 中文讲解。"</Text>
      </Box>
    </Box>
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI 赋能英语教学 · 课标锚定版</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>07 / 15</Text>
  </Box>
</Slide>
