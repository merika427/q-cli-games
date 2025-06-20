amazon Qとpygameを使用し作成したゲームになります

# インベーダーゲーム (invaders_game.py)

#### 実行
> python3 invaders_game.py

### 基本機能
- プレイヤーの宇宙船（緑色の長方形）
- 敵のインベーダー（赤色の四角形）が5行8列で配置
- プレイヤーの弾（青色）と敵の弾（白色）

### 操作方法
- 左右矢印キー：プレイヤーの移動
- スペースキー：弾の発射
- Rキー：ゲームオーバー時のリスタート

### ゲームシステム
- 敵を倒すとスコアが増加（1体につき100点）
- 敵が全滅すると次のレベルに進み、難易度が上昇
  - 敵の移動速度が速くなる
  - 敵の弾の発射頻度が上がる
- ゲームオーバー条件：
  - 敵の弾に当たる
  - 敵と接触する
  - 敵が画面下部に到達する

# テトリス (tetris_game.py)

#### 実行
> python3 tetris_game.py

### テトリスゲーム - 基本機能

1. テトリミノ（ブロック）：
   - 7種類の形状（I, O, T, L, J, S, Z）
   - それぞれ異なる色で表示
   - ランダムに出現

2. ゲームボード：
   - 10×20マスのプレイエリア
   - ブロックが積み上がる場所

3. 表示要素：
   - スコア表示
   - ゲームオーバー表示

### 操作方法
- 左矢印キー：テトリミノを左に移動
- 右矢印キー：テトリミノを右に移動
- 下矢印キー：テトリミノを下に移動（ソフトドロップ）
- 上矢印キー：テトリミノを回転
- スペースキー：ハードドロップ（一気に下まで落とす）
- Rキー：ゲームオーバー時にリスタート

### ゲームシステム

1. スコアシステム：
   - ライン消去ごとに100点加算
   - 複数ラインを同時に消すとボーナス（実装によって異なる）

2. ゲームの進行：
   - テトリミノが上から落ちてくる
   - プレイヤーが操作して位置を決める
   - 下に着地すると次のテトリミノが出現
   - 横一列が揃うとその行が消える
   - ブロックが画面上部に到達するとゲームオーバー
   
3. 難易度：
   - 時間経過とともに落下速度が上がる（レベルシステム）
   - 高レベルになるほど難しくなる
