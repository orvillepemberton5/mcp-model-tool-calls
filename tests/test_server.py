import pathlib,unittest
class T(unittest.TestCase):
 def test_tools(self):
  s=pathlib.Path("server/main.py").read_text()
  for x in ('ask_model','generate_image','list_models','User-Agent'):self.assertIn(x,s)
if __name__=='__main__':unittest.main()
