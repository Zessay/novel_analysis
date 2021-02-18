export W2V_FILE=/home/models/wordvector/sgns.literature.word.bz2
FILE="极品战兵》大纲.docx"
TO_FILE="小说标签.xlsx"

python run_process_outline.py \
  --source_dir=/home/data/corpus \
  --file_name=$FILE \
  --w2v_file=$W2V_FILE \
  --to_dir=/home/results/novel \
  --to_file=$TO_FILE