    for (auto&& [idx, passenger] : passengers | std::views::enumerate)
    {
        for (auto& other : passengers)
        {
            if (other.name == passenger.mother_name)
            {
                other.children.push_back(idx);
            }
        }
    }
    for (auto& passenger : passengers)
    {
        int grandchildren_count = 0;
        for(auto child_index: passenger.children)
        {
            auto& child = passengers[child_index];
            grandchildren_count += child.children.size();
        }
        if(grandchildren_count >= 10)
        {
            std::print("{}: {} unoka\n", passenger.name, grandchildren_count);
        }
    }