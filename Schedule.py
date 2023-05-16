import pandas as pd
from SchoolClass import SchoolClass


class Schedule:
    def __init__(self) -> None:
        self.quaters = ['Fall', 'Winter', 'Spring']
        self.main_df = pd.read_csv('class_data.csv')
        self.main_df.columns = ['Name', 'Taken', 'PR', 'F', 'W', 'S']
        self.avail_cls: dict[str, SchoolClass] = {}
        self.cls_taken: dict[str, SchoolClass] = {}
        self.anytime_cls: dict[str, SchoolClass] = {}
        self.gen_class_data()
        self.create_schedule()
        self.disp_avail_cls('Fall')

    def gen_class_data(self) -> None:
        # convert data frame to two dicts (taken and available)
        for i in range(len(self.main_df.index)):  # iter of row
            # get row as list (a single class)
            row = self.main_df.loc[i, :].values.flatten().tolist()
            # not a taken class add to avail_cls
            my_SchoolClass = SchoolClass(row[0], row[1], row[3:], row[2].split(', ') if type(row[2]) == float() else [])
            self.avail_cls[row[0]] = my_SchoolClass

        # remove class already taken from avail_cls
        # add class already taken to cls_taken
        for cls in self.avail_cls.keys():
            if self.avail_cls[cls].get_taken():
                self.cls_taken[cls] = self.avail_cls[cls]
        for cls in self.cls_taken.keys():
            if cls in self.avail_cls:
                del self.avail_cls[cls]

        # remove pre_reqs already taken
        # add post classes to avail_cls
        cls_taken_set = set(self.cls_taken.keys())
        for cls in self.avail_cls.keys():
            self.avail_cls[cls].remove_pre_req(cls_taken_set)
            for pre_req in self.avail_cls[cls].get_pre_reqs():
                self.avail_cls[pre_req].add_post_class(cls)

        # remove classes from avail_cls that can be taken at any time
        for cls in self.avail_cls.keys():
            pre_reqs = self.avail_cls[cls].get_pre_reqs()
            post_classes = self.avail_cls[cls].get_post_classes()
            if pre_reqs == post_classes == set():
                self.anytime_cls[cls] = self.avail_cls[cls]

        # del classes from avail_cls that are in anytime_cls
        for cls in self.anytime_cls.keys():
            del self.avail_cls[cls]

        # set chain length in avail_cls
        for cls in self.avail_cls.keys():
            self.get_chain_len(cls)

    def get_chain_len(self, sch_cls: str) -> int:
        if self.avail_cls[sch_cls].get_chain_len() == 0:
            if self.avail_cls[sch_cls].get_pre_reqs():
                biggest: str | None = None

                for pre_req in self.avail_cls[sch_cls].get_pre_reqs():
                    if self.avail_cls[pre_req].get_chain_len() == 0:
                        chain_len = self.get_chain_len(pre_req)
                        self.avail_cls[pre_req].set_chain_len(1+chain_len)

                for pre_req in self.avail_cls[sch_cls].get_pre_reqs():
                    def length(x): return self.avail_cls[x].get_chain_len()
                    if biggest is not None:
                        check = length(biggest) < length(pre_req)
                    else:
                        check = False
                    if biggest is None or check:
                        biggest = pre_req

                num = self.avail_cls[biggest].get_chain_len()  # type: ignore
                self.avail_cls[sch_cls].set_chain_len(1+num)

                old_chain = self.avail_cls[biggest].chain  # type: ignore
                self.avail_cls[sch_cls].chain = self.avail_cls[sch_cls].chain + old_chain
                self.avail_cls[sch_cls].chain.append(biggest)
                return num
            else:
                self.avail_cls[sch_cls].set_chain_len(1)
                return 1
        else:
            return self.avail_cls[sch_cls].get_chain_len()  # type: ignore

    def create_schedule(self):
        # look for class without a post class
        # add them to temp dict
        no_post_class: dict[str, SchoolClass] = {}
        for cls in self.avail_cls.keys():
            if not self.avail_cls[cls].get_post_classes():
                no_post_class[cls] = self.avail_cls[cls]

        keys_sorted = sorted(no_post_class.keys(),
                             key=lambda x: no_post_class[x].get_chain_len())

        for key in keys_sorted:
            print(key, self.avail_cls[key].get_chain_len(
            ), self.avail_cls[key].chain)

    def disp_avail_cls(self, quater: str):
        print()
        for cls in self.avail_cls.keys():
            if self.avail_cls[cls].offered[quater]:
                print(cls)
        print()
        for cls in self.anytime_cls.keys():
            if self.anytime_cls[cls].offered[quater]:
                print(cls)
        print()


if __name__ == '__main__':
    schd = Schedule()
    print()
    for key in schd.avail_cls.keys():
        print(schd.avail_cls[key])
    print()

    for key in schd.anytime_cls.keys():
        print(schd.anytime_cls[key])
    print()

    for key in schd.cls_taken.keys():
        print(schd.cls_taken[key])
    print()
