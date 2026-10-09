<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid #2E7D32', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'#2E7D32' }}>配套交付：资源包、提示词包、Skill 清单</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>今天发到手上，不是发一个链接让你回去自己找</Text>
  </Box>
  <Box style={{ flex:1, flexDirection:'row', gap:16, marginTop:14, alignItems:'stretch' }}>
    <Box style={{ flex:1, background:'#F4F8FA', borderRadius:12, padding:'20px 22px' }}>
      <Text style={{ fontSize:22, fontWeight:'bold', color:'#1A5F7A' }}>资源包</Text>
      <Box style={{ marginTop:12, gap:8 }}>
        {['免费 AI 工具清单及入口','提示词公式随身卡','分场景提示词速查表','分学科提示词示例集','数据安全三条提示卡'].map((s, i) => (
          <Box key={i} style={{ flexDirection:'row', gap:9, alignItems:'flex-start' }}>
            <Text style={{ fontSize:15, color:'#2E7D32', fontWeight:'bold' }}>✓</Text>
            <Text style={{ fontSize:18, color:'#1F2937', flex:1, lineHeight:1.45 }}>{s}</Text>
          </Box>
        ))}
      </Box>
    </Box>
    <Box style={{ flex:1, background:'#F4F8FA', borderRadius:12, padding:'20px 22px' }}>
      <Text style={{ fontSize:22, fontWeight:'bold', color:'#2E7D32' }}>提示词包（11 类）</Text>
      <Box style={{ flexDirection:'row', flexWrap:'wrap', gap:8, marginTop:12 }}>
        {['通用','备课','出题组卷','批改评价','学情','作业','教研','论文课题','班级管理','技能 Skill','数据安全'].map((s, i) => (
          <Box key={i} style={{ background:'#FFFFFF', borderRadius:14, padding:'7px 14px', border:'1px solid #2E7D32' }}>
            <Text style={{ fontSize:16, color:'#2E7D32', fontWeight:'bold' }}>{s}</Text>
          </Box>
        ))}
      </Box>
      <Text style={{ fontSize:17, color:'#5B6B7B', marginTop:14, lineHeight:1.55 }}>看到合适的直接抄走，改成你学科的内容就行，不用背。</Text>
    </Box>
    <Box style={{ flex:1, background:'#F4F8FA', borderRadius:12, padding:'20px 22px' }}>
      <Text style={{ fontSize:22, fontWeight:'bold', color:'#2E7D32' }}>Skill 推荐清单</Text>
      <Box style={{ marginTop:12, gap:8 }}>
        {['11 大类教师技能导航','自定义 Skill 指令模板','创建前自检清单卡','常见误区提醒'].map((s, i) => (
          <Box key={i} style={{ flexDirection:'row', gap:9, alignItems:'flex-start' }}>
            <Text style={{ fontSize:15, color:'#2E7D32', fontWeight:'bold' }}>✓</Text>
            <Text style={{ fontSize:18, color:'#1F2937', flex:1, lineHeight:1.45 }}>{s}</Text>
          </Box>
        ))}
      </Box>
    </Box>
  </Box>
  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI赋能中小学教育教学 · 县域教师培训</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>30 / 32</Text>
  </Box>
</Slide>
