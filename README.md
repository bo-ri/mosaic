## ディレクトリ構造
```
.
├── dist          // 生成したモザイク画像の出力先
├── libs
├── mongodb       // mongoのデータマウント
│   ├── diagnostic.data
│   └── journal
├── source_images // ソース画像を置いておく
│   ├── new      // 新規に追加するソース画像はnewの下に入れておく
│   └── source   // mongoにRGB情報を格納したらrenameしてnewからこっちに移動される
└── target        // ターゲットの画像
```
