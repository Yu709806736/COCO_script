# COCO 数据集标注转换
#### by Jiajun Yu on Aug. 13, 2020

### txt文件格式
(可参考[test.txt](./test.txt))
- 图片行：以“# ”（井号+空格）开头，随后为图片名称、宽度（width）和高度（height）
- category分类行：以body/face开头，空格后为一整数n，表示关键点个数，目前只支持body 17，body 12（没有头部关键点），以及face 5。随后4个整数为bounding box，格式为[x1, y1, width, height]，其中（x1, y1）为区域左上角的坐标，width和height分别为bounding box的宽度以及高度。最后一个整数为该bounding box区域中人体/人脸的个数p。
- segmentation分段行：以segmentation/seg开头，共有两种格式：
  * 如果p>1，则需要采用RLE格式，则segmentation/seg之后应为m个数，这些数的总和应为bounding box的面积（width*height）；
  * 如果p=1，则采用polygon格式，这种格式面积不好算，所以需要给出。即segmentation/seg文字之后有k个数（k为偶数），分别为k/2边形的坐标；这k个数后空格写一个“area”，再空格后为多边形面积。
- annotation标注行：共有 3np 个数，即 np 个有序数对(x, y, v)，其中(x, y)为该关键点坐标，v为其可见程度，0为无关键点，1为遮挡，2为可见。其中如果v=0，则x=y=0。
