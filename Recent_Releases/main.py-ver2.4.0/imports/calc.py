import ast


def safe_eval(expression):
    try:
        # 文字列内の '×' を '*' に、'÷' を '/' に変換
        expression = expression.replace("×", "*").replace("÷", "/").replace("^", "**").replace("××", "**")
        
        # 式を構文解析
        tree = ast.parse(expression, mode='eval')
        
        # 許可されているノードタイプのみを確認
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Expression, ast.BinOp, ast.Constant, 
                                     ast.Add, ast.Sub, ast.Mult, ast.Div, 
                                     ast.Mod, ast.Pow, ast.FloorDiv, 
                                     ast.UnaryOp, ast.USub, ast.UAdd)):
                raise ValueError("無効な演算が含まれています。")
        
        # 安全な評価を実行
        return eval(compile(tree, filename="", mode="eval"))
    
    except Exception as e:
        raise ValueError("計算エラー: 無効な式です。")
