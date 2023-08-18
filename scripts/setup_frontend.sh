react_dir=my-app
npx create-react-app $react_dir --template typescript

cp frontend/package.json $react_dir
cp frontend/src/bacon.jpg $react_dir/src
cp frontend/src/App.css $react_dir/src
cp frontend/src/App.tsx $react_dir/src
cp frontend/src/utils.tsx $react_dir/src
cp -r frontend/src/components $react_dir/src
