import {readFile,writeFile} from 'node:fs/promises';

// Whitespace-only CSS compaction. Strings and escape sequences remain byte-identical.
const source=await readFile('assets/css/styles.css','utf8');
let result='',quote='',pendingSpace=false;
for(let i=0;i<source.length;i++){
  const c=source[i],next=source[i+1];
  if(quote){
    result+=c;
    if(c==='\\'&&i+1<source.length)result+=source[++i];
    else if(c===quote)quote='';
    continue;
  }
  if(c==='/'&&next==='*'){
    const end=source.indexOf('*/',i+2);
    if(end<0)throw Error('Unclosed CSS comment');
    i=end+1;pendingSpace=true;continue;
  }
  if(/\s/.test(c)){pendingSpace=true;continue;}
  if(pendingSpace&&result&&!/[{;:]$/.test(result)&&!/[};:,]/.test(c))result+=' ';
  pendingSpace=false;
  result+=c;
  if(c==='"'||c==="'")quote=c;
}
if(quote)throw Error('Unclosed CSS string');
result=result.trim()+'\n';
await writeFile('assets/css/styles.min.css',result);
console.log(JSON.stringify({sourceBytes:Buffer.byteLength(source),minifiedBytes:Buffer.byteLength(result),fontFaces:(result.match(/@font-face/g)||[]).length}));
