import os
import shutil
import subprocess
import traceback

src = r'D:\frt.git\Tour.Product.ProductMetaService\productmeta-api\contract\Tour\Product\ProductMetaService\Client'
dst = r'D:\frt.git\SOA2CSharpClient\Tour.Product.ProductMetaService.Client\Tour\Product\ProductMetaService\Client'
build_path = r'D:\frt.git\SOA2CSharpClient\JavaSOA2CSharpClient.sln'

#copy to path
print('正在拷贝契约文件。')
for root, dirs, list in os.walk(src): 
	for i in list:
		srcfile = os.path.join(root, i)
		tarfile = os.path.join(dst, i)
		shutil.copyfile(srcfile,tarfile)

#build
print("正在生成契约。")
cmd = 'MSBuild {0} /t:Rebuild /p:Configuration=Release /m /clp:ErrorsOnly /nologo'.format(build_path)
obj = subprocess.Popen(cmd,shell=True)
obj.wait()

#copy to library path
shutil.copyfile('D:\\frt.git\SOA2CSharpClient\Tour.Product.ProductMetaService.Client\\bin\Release\Tour.Product.ProductMetaService.Client.dll','D:\\frt.git\Tour.Product.Library-Maven\Code\comservice\Tour.Product.ProductMetaService.Client.dll');
shutil.copyfile('D:\\frt.git\SOA2CSharpClient\Tour.Product.ProductMetaService.Client\\bin\Release\Tour.Product.ProductMetaService.Client.pdb','D:\\frt.git\Tour.Product.Library-Maven\Code\comservice\Tour.Product.ProductMetaService.Client.pdb');
os.system('start D:\\frt.git\Tour.Product.Library-Maven\Code\comservice')

print('契约生成完毕。')

#删除契约cs文件
for root, dirs, list in os.walk(src): 
	for i in list:
		os.remove(os.path.join(root, i))