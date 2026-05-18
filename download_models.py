"""
YOLO模型下载脚本
下载模型到项目的models目录下
"""
import os
import sys
import shutil

# 项目models目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(SCRIPT_DIR, 'models')


def download_models(output_dir=None):
    """下载所有YOLO模型到指定目录"""
    if output_dir is None:
        output_dir = MODELS_DIR

    print("=" * 60)
    print("YOLO模型下载脚本")
    print("=" * 60)
    print(f"目标目录: {output_dir}")

    # 确保目录存在
    os.makedirs(output_dir, exist_ok=True)

    try:
        from ultralytics import YOLO
    except ImportError:
        print("\n错误: 未安装ultralytics库")
        print("请先运行: pip install ultralytics")
        return

    # 要下载的模型列表
    models = [
        # YOLOv5系列
        ("yolov5n.pt", "YOLOv5 Nano", "1.9M"),
        ("yolov5s.pt", "YOLOv5 Small", "7.2M"),
        ("yolov5m.pt", "YOLOv5 Medium", "21.2M"),
        ("yolov5l.pt", "YOLOv5 Large", "46.5M"),
        ("yolov5x.pt", "YOLOv5 Extra Large", "86.7M"),

        # YOLOv8系列
        ("yolov8n.pt", "YOLOv8 Nano", "3.2M"),
        ("yolov8s.pt", "YOLOv8 Small", "11.2M"),
        ("yolov8m.pt", "YOLOv8 Medium", "25.9M"),
        ("yolov8l.pt", "YOLOv8 Large", "43.7M"),
        ("yolov8x.pt", "YOLOv8 Extra Large", "68.2M"),
    ]

    print(f"\n将下载 {len(models)} 个模型:\n")
    for weight, name, params in models:
        target_path = os.path.join(output_dir, weight)
        exists = "✓" if os.path.exists(target_path) else " "
        print(f"  [{exists}] {name} ({weight}) - {params}")

    print("\n" + "-" * 60)
    print("开始下载...\n")

    success_count = 0
    skip_count = 0
    fail_count = 0

    for i, (weight, name, params) in enumerate(models, 1):
        target_path = os.path.join(output_dir, weight)

        # 检查是否已存在
        if os.path.exists(target_path):
            print(f"[{i}/{len(models)}] {name} 已存在，跳过")
            skip_count += 1
            continue

        print(f"[{i}/{len(models)}] 下载 {name} ({weight})...")

        try:
            # 加载模型会自动下载到缓存目录
            model = YOLO(weight)

            # 获取缓存路径
            cache_path = model.ckpt_path if hasattr(model, 'ckpt_path') else None

            if cache_path and os.path.exists(cache_path):
                # 复制到目标目录
                shutil.copy2(cache_path, target_path)
                print(f"    ✓ 下载成功 -> {target_path}")
            else:
                # 尝试从默认缓存位置查找
                home = os.path.expanduser("~")
                cache_dir = os.path.join(home, ".cache", "ultralytics")
                cached_file = os.path.join(cache_dir, weight)

                if os.path.exists(cached_file):
                    shutil.copy2(cached_file, target_path)
                    print(f"    ✓ 从缓存复制 -> {target_path}")
                else:
                    # 直接保存模型
                    model.save(target_path)
                    print(f"    ✓ 保存成功 -> {target_path}")

            success_count += 1

            # 释放内存
            del model

        except Exception as e:
            print(f"    ✗ 下载失败: {e}")
            fail_count += 1

        print()

    print("=" * 60)
    print(f"下载完成!")
    print(f"  成功: {success_count}")
    print(f"  跳过: {skip_count}")
    print(f"  失败: {fail_count}")
    print(f"  模型目录: {output_dir}")
    print("=" * 60)

    # 列出目录中的模型
    print("\n当前模型文件:")
    for f in sorted(os.listdir(output_dir)):
        if f.endswith('.pt') or f.endswith('.pth'):
            size_mb = os.path.getsize(os.path.join(output_dir, f)) / (1024 * 1024)
            print(f"  {f} ({size_mb:.1f} MB)")


def download_single_model(model_name, output_dir=None):
    """下载单个模型"""
    if output_dir is None:
        output_dir = MODELS_DIR

    os.makedirs(output_dir, exist_ok=True)

    try:
        from ultralytics import YOLO
    except ImportError:
        print("错误: 未安装ultralytics库")
        print("请先运行: pip install ultralytics")
        return

    # 自动添加.pt后缀
    if not model_name.endswith('.pt') and not model_name.endswith('.pth'):
        model_name = model_name + '.pt'

    target_path = os.path.join(output_dir, model_name)

    if os.path.exists(target_path):
        print(f"模型已存在: {target_path}")
        return

    print(f"下载模型: {model_name}")
    print(f"目标路径: {target_path}")

    try:
        model = YOLO(model_name)

        # 尝试复制到目标目录
        cache_path = model.ckpt_path if hasattr(model, 'ckpt_path') else None

        if cache_path and os.path.exists(cache_path):
            shutil.copy2(cache_path, target_path)
        else:
            model.save(target_path)

        print(f"✓ 下载成功!")
        print(f"文件大小: {os.path.getsize(target_path) / (1024*1024):.1f} MB")

    except Exception as e:
        print(f"✗ 下载失败: {e}")


def list_models(output_dir=None):
    """列出所有支持的模型和已下载的模型"""
    if output_dir is None:
        output_dir = MODELS_DIR

    supported = [
        ("yolov5n.pt", "YOLOv5 Nano", "1.9M"),
        ("yolov5s.pt", "YOLOv5 Small", "7.2M"),
        ("yolov5m.pt", "YOLOv5 Medium", "21.2M"),
        ("yolov5l.pt", "YOLOv5 Large", "46.5M"),
        ("yolov5x.pt", "YOLOv5 Extra Large", "86.7M"),
        ("yolov8n.pt", "YOLOv8 Nano", "3.2M"),
        ("yolov8s.pt", "YOLOv8 Small", "11.2M"),
        ("yolov8m.pt", "YOLOv8 Medium", "25.9M"),
        ("yolov8l.pt", "YOLOv8 Large", "43.7M"),
        ("yolov8x.pt", "YOLOv8 Extra Large", "68.2M"),
    ]

    print("\n支持的YOLO模型:")
    print("-" * 60)
    print(f"{'模型文件':<18} {'名称':<25} {'参数量':<10} {'状态':<8}")
    print("-" * 60)

    for weight, name, params in supported:
        path = os.path.join(output_dir, weight)
        status = "已下载" if os.path.exists(path) else "未下载"
        print(f"{weight:<18} {name:<25} {params:<10} {status:<8}")

    print("-" * 60)

    # 显示目录中其他模型
    if os.path.exists(output_dir):
        other_models = []
        for f in os.listdir(output_dir):
            if (f.endswith('.pt') or f.endswith('.pth')) and f not in [s[0] for s in supported]:
                other_models.append(f)

        if other_models:
            print("\n其他本地模型:")
            for f in sorted(other_models):
                size_mb = os.path.getsize(os.path.join(output_dir, f)) / (1024 * 1024)
                print(f"  {f} ({size_mb:.1f} MB)")

    print(f"\n模型目录: {output_dir}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg == "--list" or arg == "-l":
            list_models()
        elif arg == "--help" or arg == "-h":
            print("用法:")
            print("  python download_models.py          # 下载所有模型到models目录")
            print("  python download_models.py yolov8n  # 下载指定模型")
            print("  python download_models.py --list   # 列出所有模型")
            print("  python download_models.py --help   # 显示帮助")
        else:
            download_single_model(arg)
    else:
        download_models()
