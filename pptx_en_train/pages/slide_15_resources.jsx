<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #1A5F7A', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#1A5F7A' }}>资源与结语：带得走、用得上</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>提示词速查卡 + 教学评一致性自检 4 问</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'row', gap:18, marginTop:14, alignItems:'stretch' }}>
    <Box style={{ flex:1, background:'#F4F8FA', borderRadius:12, padding:'18px 20px' }}>
      <Text style={{ fontSize:21, fontWeight:'bold', color:'#1A5F7A' }}>附录资源</Text>
      <Box style={{ marginTop:12, gap:10 }}>
        <Box style={{ background:'#FFFFFF', borderRadius:8, padding:'10px 14px' }}><Text style={{ fontSize:16, color:'#1F2937' }}><span style={{ fontWeight:'bold', color:'#1A5F7A' }}>A.</span> 5 册 40 单元 × 主题范畴 × 推荐方法 速查表</Text></Box>
        <Box style={{ background:'#FFFFFF', borderRadius:8, padding:'10px 14px' }}><Text style={{ fontSize:16, color:'#1F2937' }}><span style={{ fontWeight:'bold', color:'#1A5F7A' }}>B.</span> 22 张提示词速查卡（写作/口语/词汇/阅读/语法/文化/项目/评测）</Text></Box>
        <Box style={{ background:'#FFFFFF', borderRadius:8, padding:'10px 14px' }}><Text style={{ fontSize:16, color:'#1F2937' }}><span style={{ fontWeight:'bold', color:'#1A5F7A' }}>C.</span> 讲师备货清单 + 飞象老师/豆包 操作截图脚本</Text></Box>
      </Box>
      <Box style={{ marginTop:12, background:'#FFF7ED', borderRadius:8, padding:'10px 14px' }}>
        <Text style={{ fontSize:15, color:'#1F2937', lineHeight:1.5 }}>用法：自选下周单元 → 查表 → 选 1-3 个方法 → 附录 B 复制提示词。</Text>
      </Box>
    </Box>
    <Box style={{ flex:1, background:'#1A5F7A', borderRadius:12, padding:'18px 20px' }}>
      <Text style={{ fontSize:21, fontWeight:'bold', color:'#FFFFFF' }}>教学评一致性 自检 4 问</Text>
      <Box style={{ marginTop:12, gap:10 }}>
        {['目标是否对齐核心素养与主题语境？','活动是否基于真实译林版单元任务？','AI 产出是否经过学生/教师自改？','评价能否检验"教-学-评"闭环？'].map((q, i) => (
          <Box key={i} style={{ flexDirection:'row', gap:10, alignItems:'flex-start' }}>
            <Text style={{ fontSize:20, fontWeight:'bold', color:'#FBBF24', fontFamily:'Arial' }}>{i+1}</Text>
            <Text style={{ fontSize:16, color:'#EAF3F6', lineHeight:1.5, flex:1 }}>{q}</Text>
          </Box>
        ))}
      </Box>
    </Box>
  </Box>
  <Box style={{ marginTop:14, flexDirection:'row', alignItems:'center', gap:14, justifyContent:'center' }}>
    <FAIcon name='graduation-cap' style={{ fill:'#2E7D32', width:30, height:30 }} />
    <Text style={{ fontSize:22, fontWeight:'bold', color:'#1A5F7A' }}>让 AI 成为备课的脚手架，而非思考的替代品。</Text>
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI 赋能英语教学 · 课标锚定版</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>15 / 15</Text>
  </Box>
</Slide>
