class MDBQueryBuilder:
    def __init__(self):
        self.pipeline = []
        self.ranges = {"year": [None, None]}
        self.range_on = {"year": False}
        self.filters =          {"title": [], "tags":[], "authors.name":[], "language": [], "type":[], "journal": [] }
        self.filter_on=         {"title": False, "tags": False, "authors.name": False, "language": False, "type": False, "journal": False }
        self.filter_for_all =   {"title": False, "tags": False, "authors.name": False, "language": False, "type": False, "journal": False }


    def copy(self):
        ret_val = MDBQueryBuilder()
        ret_val.ranges = self.ranges.copy()
        ret_val.range_on = self.range_on.copy()
        ret_val.filters = self.filters.copy()
        ret_val.filter_on = self.filter_on.copy()
        ret_val.filter_for_all = self.filter_for_all.copy()
        return ret_val

    def _toggle_range(self, field:str):
        ret_val = self.copy()
        ret_val.range_on[field] = not self.range_on[field]
        return ret_val
    def _add_range(self, field:str, lower_bound= None, upper_bound = None):
        ret_val = self.copy()
        ret_val.ranges[field] = [lower_bound, upper_bound]
        return ret_val

    def _toggle_search_by_field(self, field:str):
        ret_val = self.copy()
        ret_val.filter_on[field] = not self.filter_on[field]
        return ret_val
    
    def _toggle_search_all_by_field(self, field:str):
        ret_val = self.copy()
        ret_val.filter_for_all[field] = not self.filter_for_all[field]
        return ret_val

    def _add_elem(self, field:str, elem:str):
        ret_val = self.copy()
        ret_val.filters[field].append(elem)
        return ret_val
    
      
    def get_query(self):
        print(self.ranges)
        print(self.range_on)
        filters_to_apply = [f'{{ "title":{{ $regex: \".*{self.filters["title"][0]}.*\" }}}}'] if self.filter_on["title"] is True else []
        filters_to_apply += [f'{{"{key}": {{{f"$gte: {val[0]}, " if val[0] is not None else "" }{f"$lte: {val[1]}" if val[1] is not None else "" } }} }}' for key, val in self.ranges.items() if self.range_on[key] is True]
        filters_to_apply += [f'{{"{key}": {{ {"$all" if self.filter_for_all[key] is True else "$in"}: {val}}}}}' for key, val in self.filters.items() if self.filter_on[key] is True and key != "title"] 
        pipeline = "db.papers.find({$and: [" + ",".join(filters_to_apply) + "]})"
        return (pipeline)


#db.papers.find({"authors.name": {$all: ['Paul Kocher', ]}}) all articles written by the following authors at the same time
# db.papers.find({"authors.name": {$in: ['Paul Kocher', "ciro"]}}) all articles written by at least one of these authors
#db.papers.find({$and: [{"authors.name": {$in: ['Paul Kocher', "ciro"]}}, {"type": "article"}]})


b = MDBQueryBuilder()
b = b\
    ._toggle_search_by_field("title")\
    ._add_elem("title",'down' )\
    ._toggle_search_by_field("authors.name")\
    ._toggle_search_all_by_field("authors.name")\
    ._add_elem("authors.name",'Paul Kocher')\
    ._add_elem("authors.name",'Daniel Genkin')\
    ._toggle_search_by_field("type")\
    ._add_elem("type", "article")\
    ._toggle_range("year")\
    ._add_range("year",1915, 2018)\
    ._toggle_search_by_field("journal")\
    ._add_elem("journal", 'meltdownattack.com')\
    .get_query()
print(b)

#print(MDBQueryBuilder()._toggle_search_by_field("language")._toggle_search_all_by_field("language")._add_elem("language", "english")._add_elem("language", "afrikaans").get_query())
#print(MDBQueryBuilder()._toggle_search_by_field("journal")._add_elem("journal", 'meltdownattack.com').get_query())
#db.papers.aggregate([{$unwind: {path: "$authors"}}, {$group: {_id: "$authors.name", "count": {$sum: 1}, "has_written": {$push: "$title"}}}])

#db.papers.aggregate([{$unwind: {path: "$authors"}}, {$group: {_id: {"author": "$authors", "lang": {$ifNull: ["$language", "unknown"]}},"count": {$sum: 1}, "works": {$push: "$title"}}}, {$group: {_id:"$_id.author", "work_by_lang": {$push: {"lang": "$_id.lang", "count": "$count", "works": "$works"}}}}])