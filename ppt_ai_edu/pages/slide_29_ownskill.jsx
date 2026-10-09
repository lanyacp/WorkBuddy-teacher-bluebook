<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #F57C00', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#C2410C' }}>把自己的经验沉淀成 Skill</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>全场最能带走的一页。创建前先想清四件事</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'row', gap:16, marginTop:16, alignItems:'stretch' }}>
    <Box style={{ flex:1.2, flexDirection:'column', gap:11 }}>
      {[{n:'1',t:'触发场景',d:'什么时候用？例：单元考前出卷',c:'#1A5F7A'},
        {n:'2',t:'输入材料',d:'需要我提供什么？教材版本、单元、学生错题数据',c:'#1A5F7A'},
        {n:'3',t:'产出形态',d:'要什么文件？Word 试卷 / 错题集 / 提纲',c:'#2E7D32'},
        {n:'4',t:'质量标准',d:'好用的标准是什么？含答案、难度梯度、贴合本校学情',c:'#2E7D32'}].map((o, i) => (
        <Box key={i} style={{ flex:1, flexDirection:'row', alignItems:'center', gap:14, background:'#F4F8FA', borderRadius:10, padding:'12px 18px' }}>
          <Box style={{ width:36, height:36, borderRadius:18, background:o.c, alignItems:'center', justifyContent:'center' }}>
            <Text style={{ fontSize:18, color:'#fff', fontWeight:'bold', fontFamily:'Arial' }}>{o.n}</Text>
          </Box>
          <Box style={{ flex:1 }}>
            <Text style={{ fontSize:20, fontWeight:'bold', color:o.c }}>{o.t}</Text>
            <Text style={{ fontSize:17, color:'#1F2937', marginTop:3, lineHeight:1.4 }}>{o.d}</Text>
          </Box>
        </Box>
      ))}
    </Box>
    <Box style={{ flex:1, background:'#1F2937', borderRadius:12, padding:'20px 22px' }}>
      <Text style={{ fontSize:19, color:'#FBBF24', fontWeight:'bold' }}>指令模板（填空即用）</Text>
      <Text style={{ fontSize:18, color:'#E5E7EB', marginTop:12, lineHeight:1.8 }}>角色：你是一位有 __ 年经验的【学科】命题教师。<br /><br />任务：根据【教材版本 + 年级 + 单元】，生成【试卷 / 错题集 / 提纲】。<br /><br />要求：① 题型含 __；② 重点覆盖 __；③ 每题附答案与解析；④ 贴合本校学情。</Text>
      <Box style={{ marginTop:14, borderTop:'1px solid #374151', paddingTop:10 }}>
        <Text style={{ fontSize:16, color:'#9CA3AF', fontStyle:'italic', lineHeight:1.5 }}>五步流程：创建入口 → 填基本信息（名称用「学科+用途+年级」）→ 写指令模板 → 保存测试 → 按产出迭代。第一版通常要调 2-3 次。</Text>
      </Box>
    </Box>
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI赋能中小学教育教学 · 县域教师培训</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>29 / 32</Text>
  </Box>
</Slide>
