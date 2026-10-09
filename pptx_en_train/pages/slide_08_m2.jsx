<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #1A5F7A', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#1A5F7A' }}>M2 写作协同 ＋ 推荐信实战</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>课标锚点：人与自我·做人与做事 ｜ 核心素养：语言/思维/文化 ｜ 真实单元：九上U1 Know yourself</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'row', gap:18, marginTop:14, alignItems:'stretch' }}>
    <Box style={{ flex:1, background:'#F4F8FA', borderRadius:12, padding:'18px 20px' }}>
      <Text style={{ fontSize:22, fontWeight:'bold', color:'#1A5F7A' }}>四步实操</Text>
      {['拆解九上U1 D2 范信结构（开头-主体-结尾-礼貌语）','豆包生成"推荐班长/学习委员"两版底稿','教师用红笔自改（标 3 个可替换点）','飞象老师/PPT 展示，对照原版范信微调'].map((s, i) => (
        <Box key={i} style={{ flexDirection:'row', gap:10, alignItems:'flex-start', marginTop:14 }}>
          <Box style={{ width:28, height:28, borderRadius:14, background:'#1A5F7A', alignItems:'center', justifyContent:'center' }}><Text style={{ fontSize:15, color:'#fff', fontWeight:'bold' }}>{i+1}</Text></Box>
          <Text style={{ fontSize:17, color:'#1F2937', lineHeight:1.5, flex:1 }}>{s}</Text>
        </Box>
      ))}
      <Box style={{ marginTop:14, background:'#FFF7ED', borderRadius:8, padding:'12px 14px' }}>
        <Text style={{ fontSize:16, color:'#1F2937', lineHeight:1.5 }}>延展：七下U3 / 八下U1 → 让豆包生成"家乡变化"双语文案，用于项目布展。</Text>
      </Box>
    </Box>
    <Box style={{ flex:1.1, background:'#1F2937', borderRadius:12, padding:'18px 20px' }}>
      <Text style={{ fontSize:18, fontWeight:'bold', color:'#FBBF24' }}>豆包 / DeepSeek 提示词（九上U1）</Text>
      <Text style={{ fontSize:15, color:'#E5E7EB', lineHeight:1.7, marginTop:12 }}>你是一名初中英语教师。请根据九上U1 D2 范文（写给 Mr Wu 推荐 David 当学生会主席），生成一份【学习委员】推荐信。</Text>
      <Text style={{ fontSize:15, color:'#FBBF24', lineHeight:1.7, marginTop:10 }}>要求：</Text>
      <Text style={{ fontSize:15, color:'#E5E7EB', lineHeight:1.7 }}>① 80-100 词<br />② 结构完整（开头介绍目的 / 2-3 个品质 / 总结 / 礼貌署名）<br />③ 语言适合九年级，可直接做范例<br />④ 标出 3 个可替换点，便于课堂改编</Text>
      <Box style={{ marginTop:14, borderTop:'1px solid #374151', paddingTop:10 }}>
        <Text style={{ fontSize:14, color:'#9CA3AF', fontStyle:'italic' }}>底线：AI 出稿 → 教师/学生必须自改；写完后回到范信对照，避免风格漂移。</Text>
      </Box>
    </Box>
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI 赋能英语教学 · 课标锚定版</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>08 / 15</Text>
  </Box>
</Slide>
