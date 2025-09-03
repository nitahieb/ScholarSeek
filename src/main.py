from analyzer import ArticleAnalyzer
from pipeline import Pipeline

#TODO I'll probably make this a simple console tool once it's more formed
pipeline = Pipeline("")
pipeline.addSearch("nano+particles",retmax=2)
analyzer = ArticleAnalyzer()
pipeline.addFetch(analyzer=analyzer)
results = pipeline.getResults()
print(results.isEmpty())
